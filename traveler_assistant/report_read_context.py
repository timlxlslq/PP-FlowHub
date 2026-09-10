"""Request-local report reuse and explicit hardware-source choices.

Nothing survives the request or writes to disk. Cached results are copied so
one validation pass cannot mutate the source facts used by another pass.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from dataclasses import dataclass, field
from functools import wraps
from pathlib import Path
import time
import inspect


@dataclass
class ReportReadContext:
    choices: dict = field(default_factory=dict)
    source_conflicts: dict = field(default_factory=dict)
    resolved_sources: dict = field(default_factory=dict)
    resolved_paths: dict = field(default_factory=dict)
    parsed: dict = field(default_factory=dict)
    directories: dict = field(default_factory=dict)
    timings: list = field(default_factory=list)
    cache_hits: int = 0


_current = ContextVar('report_read_context', default=None)


def current_report_context():
    return _current.get()


@contextmanager
def report_read_session(choices=None):
    context = ReportReadContext(choices=dict(choices or {}))
    token = _current.set(context)
    try:
        yield context
    finally:
        _current.reset(token)


def preview_read_session(function):
    @wraps(function)
    def run(*args, **kwargs):
        with report_read_session(kwargs.get('hardware_source_choices')) as context:
            result = function(*args, **kwargs)
            if isinstance(result, dict):
                result['report_read_metrics'] = {
                    'cache_hits': context.cache_hits, 'files': context.timings,
                }
            return result
    return run


def report_paths(folder: Path):
    context = _current.get()
    key = str(folder)
    if context is None:
        return list(folder.rglob('*.xlsx'))
    if key not in context.directories:
        context.directories[key] = list(folder.rglob('*.xlsx'))
    return list(context.directories[key])


def cached_report(function):
    signature = inspect.signature(function)
    @wraps(function)
    def read(*args, **kwargs):
        context = _current.get()
        if context is None:
            return function(*args, **kwargs)
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        if bound.arguments.get('allow_missing_factory') is False:
            bound.arguments['fallback_factory'] = ''
        path = next(value for value in bound.arguments.values() if isinstance(value, Path))
        stamp = path.stat()
        key = (function.__module__, function.__name__, repr(bound.arguments),
               stamp.st_mtime_ns, stamp.st_size)
        if key in context.parsed:
            context.cache_hits += 1
            return deepcopy(context.parsed[key])
        started = time.perf_counter()
        result = function(*args, **kwargs)
        after = path.stat()
        if (after.st_mtime_ns, after.st_size) != (stamp.st_mtime_ns, stamp.st_size):
            raise ValueError(f'读取期间报表发生变化，请重新预览：{path}')
        context.timings.append({'path': str(path), 'reader': function.__name__,
                               'duration_seconds': round(time.perf_counter() - started, 6)})
        context.parsed[key] = deepcopy(result)
        return result
    return read
