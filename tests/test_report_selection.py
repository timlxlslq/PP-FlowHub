import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError, parse_fittings_groups
from traveler_assistant.fittings import select_latest_fittings
from traveler_assistant.order_workflow import _factory_names, _choose_fittings
from traveler_assistant.order_index import OrderIndexStore, preview_server_changes
from traveler_assistant.report_read_context import report_read_session
from traveler_assistant.streaming_process import run_with_progress
from tests.test_order_workflow import make_fittings


class ReportSelectionTests(unittest.TestCase):
    def test_changed_choice_requires_reselection_and_identical_content_deduplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = [root / 'main' / 'Fittingslist.xlsx', root / 'room leftovers' / 'Fittingslist.xlsx']
            for path, qty in zip(paths, (2, 5)):
                path.parent.mkdir()
                make_fittings(path, [('F100', qty)])
            with self.assertRaises(RuleError) as error:
                _choose_fittings(root)
            chosen = error.exception.context['conflicts'][0]['candidates'][0]
            make_fittings(Path(chosen['path']), [('F100', 9)])
            with report_read_session({'F100': chosen['id']}):
                with self.assertRaises(RuleError):
                    _choose_fittings(root)
            for path in paths:
                make_fittings(path, [('F100', 2)])
            selected, _ = _choose_fittings(root)
            self.assertEqual(selected['F100'][0].quantity, 2)

    def test_choices_apply_per_factory_in_multiblock_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a, b = root / 'Fittingslist-a.xlsx', root / 'Fittingslist-b.xlsx'
            make_fittings(a, [('F100', 2), ('F200', 3)])
            make_fittings(b, [('F100', 5), ('F200', 7)])
            with self.assertRaises(RuleError) as error:
                select_latest_fittings([a, b])
            choices = {}
            for conflict in error.exception.context['conflicts']:
                path = a if conflict['factory_order'] == 'F100' else b
                choices[conflict['factory_order']] = next(c['id'] for c in conflict['candidates'] if c['path'] == str(path.resolve()))
            with report_read_session(choices):
                selected, _, _, _ = select_latest_fittings([a, b])
            self.assertEqual({f: s.items[0].quantity for f, s in selected.items()}, {'F100': 2, 'F200': 7})

    def test_database_ownership_precedes_display_prefix_and_no_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = Config(state_dir=root / 'state')
            config.prepare_storage()
            store = OrderIndexStore(config.workflow_database)
            store.upsert_order('PP9999')
            store.upsert_order('PP8888')
            store.upsert_factory('F100', order_id='PP9999', factory_name='Closet without order prefix', ownership_status='已确认')
            store.upsert_factory('F200', order_id='PP8888', factory_name='PP9999 misleading prefix', ownership_status='已确认')
            store.commit()
            store.close()
            with patch('traveler_assistant.order_workflow.lookup_aimes_names', side_effect=AssertionError('unexpected network')):
                names, _ = _factory_names(config, root, {'F100', 'F200'}, 'PP9999')
            self.assertEqual(names, {'F100': 'Closet without order prefix'})

    def test_report_cache_is_request_local_copied_and_file_change_sensitive(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'Fittingslist.xlsx'
            make_fittings(path, [('F100', 2)])
            with report_read_session() as context:
                first = parse_fittings_groups(path)
                first.clear()
                self.assertEqual(parse_fittings_groups(path)[0][1][0].quantity, 2)
                self.assertEqual(context.cache_hits, 1)
                make_fittings(path, [('F100', 5)])
                self.assertEqual(parse_fittings_groups(path)[0][1][0].quantity, 5)
            with report_read_session() as context:
                parse_fittings_groups(path)
                self.assertEqual(context.cache_hits, 0)

    def test_process_progress_delivered_before_exit_and_timeout_kills_child(self):
        observed = []
        started = time.monotonic()
        result = run_with_progress(
            [sys.executable, '-c', 'import sys,time; sys.stdin.read(); print("progress", file=sys.stderr, flush=True); time.sleep(.5); print("{}")'],
            input_text='{}', env=os.environ.copy(), timeout=5,
            on_stderr_line=lambda line: observed.append((line, time.monotonic() - started)))
        self.assertEqual(result.stdout.strip(), '{}')
        self.assertEqual(observed[0][0], 'progress')
        self.assertGreater(time.monotonic() - started - observed[0][1], .3)
        import subprocess
        with self.assertRaises(subprocess.TimeoutExpired):
            run_with_progress([sys.executable, '-c', 'import time; time.sleep(5)'],
                              input_text='', env=os.environ.copy(), timeout=.1,
                              on_stderr_line=lambda line: None)

    def test_aimes_adapter_forwards_live_events_to_app_stderr(self):
        import io, json, subprocess
        from contextlib import redirect_stderr
        from traveler_assistant.core import _run_aimes_lookup
        output = io.StringIO()
        def process(*args, **kwargs):
            kwargs['on_stderr_line'](json.dumps({'event': 'progress', 'message': '查询工厂单名称'}))
            self.assertIn('查询工厂单名称', output.getvalue())
            return subprocess.CompletedProcess(args, 0, '{"F100":"PP9999"}', '')
        with patch('traveler_assistant.core.subprocess.check_output', return_value='test-secret'), patch('traveler_assistant.core.run_with_progress', side_effect=process), redirect_stderr(output):
            result = _run_aimes_lookup(Config(aimes_username='test'), ['F100'])
        self.assertEqual(result['F100'], 'PP9999')
        self.assertNotIn('test-secret', output.getvalue())

    def test_zero_quantity_report_is_not_silently_discarded(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / 'Fittingslist-a.xlsx', Path(temp) / 'Fittingslist-b.xlsx']
            for path, qty in zip(paths, (0, 2)):
                make_fittings(path, [('F100', qty)])
            with self.assertRaises(RuleError) as error:
                select_latest_fittings(paths)
            self.assertEqual(error.exception.code, 'fittings_selection_required')
