"""Persist user-approved hardware sources only with confirmed business writes."""
import hashlib
import json
import sqlite3


def decision_revision(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest() if value else ''


def load_source_decisions(config):
    connection = config.workflow_connection
    owns = connection is None
    if connection is None:
        if not config.workflow_database.is_file():
            return {}
        connection = sqlite3.connect(f'file:{config.workflow_database}?mode=ro', uri=True)
    try:
        if not connection.execute("select 1 from sqlite_master where name='hardware_source_decisions'").fetchone():
            return {}
        return {factory: json.loads(value) for factory, value in connection.execute(
            'select factory_order, decision_json from hardware_source_decisions')}
    finally:
        if owns:
            connection.close()


def commit_source_decisions(connection, payload, factories, skipped_orders):
    from .core import RuleError
    proposals = payload.get('hardware_source_decisions', {})
    bases = payload.get('hardware_source_decision_bases', {})
    eligible = {str(row.get('factory_order', '')).upper() for row in payload.get('write_records', {}).get('factory_orders', [])
                if str(row.get('order_id', '')).upper() not in skipped_orders} & set(factories)
    for factory in eligible:
        current = connection.execute('select decision_json from hardware_source_decisions where factory_order=?', (factory,)).fetchone()
        old = json.loads(current[0]) if current else None
        proposal = proposals.get(factory)
        if old and proposal is None:
            if payload.get('include_hardware', True):
                raise RuleError('hardware_source_stale', f'{factory} 已固定五金来源，请重新预览后确认')
            continue
        if proposal is None:
            continue
        if decision_revision(old) != bases.get(factory, '') and old != proposal:
            raise RuleError('hardware_source_stale', f'{factory} 的五金来源记录已更新，请重新预览')
        connection.execute('insert into hardware_source_decisions(factory_order, decision_json) values(?,?) '
                           'on conflict(factory_order) do update set decision_json=excluded.decision_json',
                           (factory, json.dumps(proposal, ensure_ascii=False, sort_keys=True)))


def with_source_decisions(function):
    """Apply confirmed source locks to legacy sync/Traveler entry points too."""
    from functools import wraps
    @wraps(function)
    def run(config, *args, **kwargs):
        from .report_read_context import current_report_context, report_read_session
        if current_report_context() is not None:
            return function(config, *args, **kwargs)
        with report_read_session() as context:
            # These entry points may create material/Traveler files during the
            # operation; only read-only Server previews cache directory lists.
            context.reuse_reports = False
            context.locked_decisions = load_source_decisions(config)
            return function(config, *args, **kwargs)
    return run
