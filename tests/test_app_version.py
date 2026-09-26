"""版本回归只读取隔离 plist，不编译 App，也不访问真实安装包。"""

import plistlib
import tempfile
import unittest
from pathlib import Path

from tools.app_version import next_version


class AppVersionTests(unittest.TestCase):
    def test_patch_minor_and_repeated_builds(self):
        """小修改递增末位，较大功能递增中间位；保存后再次编译继续递增。"""
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.plist"
            source.write_bytes(plistlib.dumps({"CFBundleShortVersionString": "0.4.1"}))
            self.assertEqual(next_version(source), "0.4.2")
            self.assertEqual(next_version(source, bump="minor"), "0.5.0")
            source.write_bytes(plistlib.dumps({"CFBundleShortVersionString": "0.5.0"}))
            self.assertEqual(next_version(source), "0.5.1")

    def test_existing_packages_prevent_version_regression(self):
        """按数字比较版本，旧源码或较旧安装包不能使新产物版本倒退。"""
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / name for name in ("source", "built", "installed")]
            for path, version in zip(paths, ("0.4.1", "0.4.10", "0.4.9")):
                path.write_bytes(plistlib.dumps({"CFBundleShortVersionString": version}))
            self.assertEqual(next_version(*paths), "0.4.11")
            self.assertEqual(next_version(*paths, bump="minor"), "0.5.0")

    def test_first_install_and_invalid_metadata(self):
        """未安装时正常升级；缺失源码、损坏版本和未知升级方式应拒绝。"""
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.plist"
            missing = Path(directory) / "missing.plist"
            source.write_bytes(plistlib.dumps({"CFBundleShortVersionString": "0.4.1"}))
            self.assertEqual(next_version(source, missing), "0.4.2")
            with self.assertRaises(FileNotFoundError):
                next_version(missing)
            with self.assertRaises(ValueError):
                next_version(source, bump="unknown")
            for value in ("", "0.4", "0.-4.1", "abc", 5):
                source.write_bytes(plistlib.dumps({"CFBundleShortVersionString": value}))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    next_version(source)
