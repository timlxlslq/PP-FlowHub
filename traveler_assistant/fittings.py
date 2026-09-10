"""Shared Fittingslist selection rules.

Fittingslist files can be copied into several room folders while retaining the
same factory-order blocks.  This module is deliberately independent of
Traveler generation so database synchronization and on-demand Traveler
rendering use the same source-selection contract.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable, Iterable

from .core import FittingItem, RuleError, parse_fittings_groups
from .report_read_context import current_report_context


EPSILON = 1e-9


def is_fittings_report(path: Path) -> bool:
    """Recognize current English and legacy Chinese AICNC report filenames."""
    return (
        path.suffix.casefold() == ".xlsx"
        and not path.name.startswith("~$")
        and path.stem.casefold().startswith(("fittingslist", "五金料单"))
    )


def fitting_signature(items: Iterable[FittingItem]) -> tuple:
    return tuple(sorted(
        (
            str(item.name or "").strip(),
            str(item.code or "").strip().upper(),
            str(item.size or "").strip(),
            str(item.unit or "").strip(),
            round(float(item.quantity), 6),
        )
        for item in items
    ))


@dataclass(frozen=True)
class SelectedFittings:
    path: Path
    modified_at: float
    items: tuple[FittingItem, ...]
    signature: tuple


def select_latest_fittings(
    paths: Iterable[Path],
    *,
    allow_missing_factory: bool = False,
    fallback_factory: str = "",
    is_empty_report: Callable[[Path], bool] | None = None,
) -> tuple[dict[str, SelectedFittings], list[str], bool, list[Path]]:
    """Select one complete report block per factory, requiring a choice on conflicts.

    Returns ``(selected, warnings, found_files, skipped_empty_files)``.  A
    differing report always requires an explicit content-bound choice; neither
    folder names nor modification times determine the selected source.
    """
    occurrences: dict[str, list[SelectedFittings]] = {}
    found_files = False
    skipped_empty: list[Path] = []
    for path in sorted({Path(path) for path in paths}, key=lambda item: str(item).casefold()):
        found_files = True
        try:
            groups = parse_fittings_groups(
                path,
                allow_missing_factory=allow_missing_factory,
                fallback_factory=fallback_factory,
            )
        except RuleError:
            if is_empty_report is not None and is_empty_report(path):
                skipped_empty.append(path)
                continue
            raise
        modified_at = path.stat().st_mtime
        for factory, items in groups:
            candidate = SelectedFittings(
                path=path,
                modified_at=modified_at,
                items=tuple(items),
                signature=fitting_signature(items),
            )
            occurrences.setdefault(factory.upper(), []).append(candidate)

    selected: dict[str, SelectedFittings] = {}
    warnings: list[str] = []
    conflicts: list[dict] = []
    context = current_report_context()
    choices = context.choices if context else {}
    for factory, matches in sorted(occurrences.items()):
        candidates = [fittings_candidate(source) for source in matches]
        requested = choices.get(factory)
        locked = context.locked_decisions.get(factory) if context else None
        if locked:
            chosen_data = locked['selected']
            observed = sorted({candidate['content_fingerprint'] for candidate in candidates})
            keep_id = 'keep:' + hashlib.sha256(json.dumps([factory, observed], sort_keys=True).encode()).hexdigest()
            if context.decisions_prepared:
                proposal = context.decision_proposals.get(factory, locked)
                chosen_data = proposal['selected']
            elif observed != locked.get('observed_contents', []):
                keep = dict(chosen_data, id=keep_id, label='保留已确认五金')
                updates = [c for c in candidates if c['content_fingerprint'] not in locked.get('observed_contents', [])
                           or (c['path'] == chosen_data['path'] and c['content_fingerprint'] != chosen_data['content_fingerprint'])]
                selected_candidate = next((c for c in updates if c['id'] == requested), None)
                if requested == keep_id or not updates:
                    context.keep_factories.add(factory)
                elif selected_candidate:
                    chosen_data = selected_candidate
                else:
                    conflicts.append({'factory_order': factory, 'mode': 'update',
                                      'candidates': [keep] + [dict(c, label='更新为此报表') for c in updates]})
                    continue
                context.decision_proposals[factory] = {'selected': chosen_data, 'observed_contents': observed}
            else:
                # A stable set of report contents never reopens source selection.
                context.keep_factories.add(factory)
                context.decision_proposals[factory] = locked
            selected[factory] = selected_from_candidate(chosen_data)
            continue
        resolved = context.resolved_sources.get(factory) if context else None
        # A folder-local pass cannot replace the choice resolved from the full
        # request's candidate set with another report for the same factory.
        chosen = next((source for source, candidate in zip(matches, candidates)
                       if candidate["id"] == (requested or resolved)), None)
        if resolved and chosen is None and context.resolved_paths.get(factory) not in {c["path"] for c in candidates}:
            continue
        different = len({source.signature for source in matches}) > 1
        if different and context is not None:
            context.source_conflicts[factory] = {"factory_order": factory, "candidates": candidates}
        if (different or requested or resolved) and chosen is None:
            conflicts.append({"factory_order": factory, "candidates": candidates})
            continue
        selected[factory] = chosen or matches[0]
        if context is not None:
            if not context.decisions_prepared:
                context.decision_proposals[factory] = {
                    'selected': fittings_candidate(selected[factory]),
                    'observed_contents': sorted({candidate['content_fingerprint'] for candidate in candidates}),
                }
            context.resolved_sources[factory] = fittings_candidate(selected[factory])["id"]
            context.resolved_paths[factory] = str(selected[factory].path.resolve())
        if different:
            warnings.append(f"{factory} 五金内容不一致，已采用用户选择的 {selected[factory].path}")
        elif len(matches) > 1:
            warnings.append(f"{factory} 在 {len(matches)} 份五金报表中内容一致，已自动去重")
    if conflicts:
        raise RuleError("fittings_selection_required", "同一工厂单的五金报表内容不同，请选择五金来源",
                        conflicts=conflicts)
    return selected, warnings, found_files, skipped_empty


def fittings_candidate(source: SelectedFittings) -> dict:
    """Bind a choice to the full report path and parsed content, not its time."""
    identity = json.dumps([str(source.path.resolve()), source.signature], ensure_ascii=False)
    return {
        "id": hashlib.sha256(identity.encode()).hexdigest(),
        "content_fingerprint": hashlib.sha256(json.dumps(source.signature, ensure_ascii=False).encode()).hexdigest(),
        "path": str(source.path.resolve()),
        "modified_at": source.modified_at,
        "items": [dict(name=item.name, code=item.code, spec=item.size,
                       unit=item.unit, quantity=item.quantity) for item in source.items],
    }


def selected_from_candidate(candidate):
    items = tuple(FittingItem(name=row['name'], code=row.get('code', ''), size=row.get('spec', ''),
                              unit=row.get('unit', ''), quantity=float(row['quantity']))
                  for row in candidate['items'])
    return SelectedFittings(Path(candidate['path']), candidate.get('modified_at', 0), items, fitting_signature(items))
