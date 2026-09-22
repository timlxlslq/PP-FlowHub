"""Keep shared-order discovery complete without stat-ing every CNC asset."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from traveler_assistant.order_workflow import related_order_ids
from traveler_assistant.report_read_context import cached_report, report_paths, report_read_session


class PreviewDiscoveryTests(unittest.TestCase):
    def test_shared_orders_nested_files_and_request_lifetime(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'PP0035'
            nested = root / 'New Nesting' / 'layout'
            nested.mkdir(parents=True)
            (nested / 'PP0035-2 panels.xml').touch()
            (root / 'material.xlsx').touch()
            (root / 'PP9999').mkdir()  # A directory name is not order evidence.
            (root / 'PP8888 broken.xml').symlink_to(root / 'missing')
            (root / 'PP7777 linked.xml').symlink_to(root / 'material.xlsx')
            for index in range(200):
                (nested / f'image-{index}.png').touch()
            original_is_file = Path.is_file
            checks = []

            def checked(path):
                checks.append(path.name)
                return original_is_file(path)

            with report_read_session() as context, patch.object(Path, 'is_file', checked):
                self.assertEqual(report_paths(root), [root / 'material.xlsx'])
                result = related_order_ids(root)
                self.assertEqual(result, ['PP0035', 'PP0035-2', 'PP7777'])
                result.clear()  # Caller mutation must not alter the shared result.
                self.assertEqual(related_order_ids(root), ['PP0035', 'PP0035-2', 'PP7777'])
                self.assertEqual(len(checks), 4)
                self.assertFalse(any(name.endswith('.png') for name in checks))
                self.assertEqual(len([row for row in context.discovery_timings
                                      if row['stage'] == 'directory_discovery']), 1)
                (nested / 'PP0035-3 material.xlsx').touch()
            with report_read_session():
                self.assertIn('PP0035-3', related_order_ids(root))
                self.assertEqual(len(report_paths(root)), 2)

    def test_report_change_is_rechecked_despite_directory_reuse(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'material.xlsx'
            path.write_text('first')

            @cached_report
            def read(source):
                return source.read_text()

            with report_read_session():
                report_paths(path.parent)
                self.assertEqual(read(path), 'first')
                path.write_text('changed content')
                self.assertEqual(read(path), 'changed content')

            @cached_report
            def unstable(source):
                source.write_text('changed during read')
                return 'old'

            with report_read_session(), self.assertRaisesRegex(ValueError, '读取期间报表发生变化'):
                unstable(path)
