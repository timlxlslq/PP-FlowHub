"""共享的五金报表来源选择规则。

同一工厂单的五金报表可能被复制到多个房间目录。本模块独立于 Traveler
生成流程，使数据库同步和按需生成 Traveler 使用相同的来源选择规则。
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
    """判断 path 是否为五金报表，兼容新英文及旧中文文件名，并排除临时文件。"""
    return (
        path.suffix.casefold() == ".xlsx"
        and not path.name.startswith("~$")
        and path.stem.casefold().startswith(("fittingslist", "五金料单"))
    )


def fitting_signature(items: Iterable[FittingItem]) -> tuple:
    """标准化并排序五金记录以比较内容；items 为记录集合，数量保留六位小数。"""
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
    """为每个工厂单选取完整五金记录，内容冲突时要求明确选择。

    参数：paths 为候选报表路径；allow_missing_factory 决定是否允许缺少工厂单号；
    fallback_factory 为缺号时的替代单号；is_empty_report 为可选空报表判断函数。
    返回所选记录、警告、是否找到文件及跳过的空报表。来源选择绑定内容，
    不能仅凭目录名称或修改时间决定采用哪份报表。
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
        if locked and locked.get('handling') == 'manual':
            report_versions = {str(source.path.resolve()): hashlib.sha256(source.path.read_bytes()).hexdigest() for source in matches}
            confirmed_versions = {str(Path(path).resolve()): value for path, value in locked.get('report_versions', {}).items()}
            if report_versions and all(confirmed_versions.get(path) == value for path, value in report_versions.items()):
                context.keep_factories.add(factory)
                context.decision_proposals[factory] = locked
                source = matches[0]
                selected[factory] = SelectedFittings(source.path, source.modified_at, (), ())
                continue
            # 报表变化后必须重新明确选择，包括仅字节变化；不能沿用人工处理豁免。
            if not requested:
                conflicts.append({'factory_order': factory, 'mode': 'update',
                                  'candidates': [dict(c, label='重新核对并采用此报表') for c in candidates]})
                continue
            locked = None
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
                # 报表内容集合未变时，不重新要求选择来源。
                context.keep_factories.add(factory)
                context.decision_proposals[factory] = locked
            selected_source = next(
                (
                    source
                    for source in matches
                    if fittings_candidate(source)["content_fingerprint"]
                    == chosen_data.get("content_fingerprint", "")
                ),
                None,
            )
            selected[factory] = selected_source or selected_from_candidate(chosen_data)
            continue
        resolved = context.resolved_sources.get(factory) if context else None
        # 单个目录内的读取不能用另一份报表替换完整请求已经确定的工厂单来源。
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
        raise RuleError("fittings_selection_required", "Server 五金报表来源或版本变化，请重新核对并选择五金来源",
                        conflicts=conflicts, source="Server 五金报表",
                        factory_orders=[row["factory_order"] for row in conflicts],
                        source_paths=sorted({candidate["path"] for row in conflicts for candidate in row["candidates"]}))
    return selected, warnings, found_files, skipped_empty


def fittings_candidate(source: SelectedFittings) -> dict:
    """把来源绑定到完整路径及解析内容；source 为所选五金报表，修改时间不参与标识计算。"""
    identity = json.dumps([str(source.path.resolve()), source.signature], ensure_ascii=False)
    return {
        "id": hashlib.sha256(identity.encode()).hexdigest(),
        "content_fingerprint": hashlib.sha256(json.dumps(source.signature, ensure_ascii=False).encode()).hexdigest(),
        "path": str(source.path.resolve()),
        "modified_at": source.modified_at,
        "items": [dict(name=item.name, code=item.code, spec=item.size,
                       unit=item.unit, quantity=item.quantity) for item in source.items],
    }


def same_selected_fittings_source(source: SelectedFittings, path: Path, items: Iterable[FittingItem] | None = None) -> bool:
    """检查报表是否仍对应已确认来源；source 为已选来源，path 为当前路径，items 为可选的当前解析条目。路径大小写变化不会视为来源变化。"""
    selected = Path(source.path)
    current = Path(path)
    try:
        if selected.samefile(current):
            return True
    except OSError:
        pass
    if selected.resolve() == current.resolve():
        return True
    return items is not None and fitting_signature(items) == source.signature


def selected_from_candidate(candidate):
    """从候选字典 candidate 还原所选五金报表及内容签名，缺省修改时间记为零。"""
    items = tuple(FittingItem(name=row['name'], code=row.get('code', ''), size=row.get('spec', ''),
                              unit=row.get('unit', ''), quantity=float(row['quantity']))
                  for row in candidate['items'])
    return SelectedFittings(Path(candidate['path']), candidate.get('modified_at', 0), items, fitting_signature(items))
