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
        "path": str(source.path.resolve()),
        "modified_at": source.modified_at,
        "items": [dict(name=item.name, code=item.code, spec=item.size,
                       unit=item.unit, quantity=item.quantity) for item in source.items],
    }
