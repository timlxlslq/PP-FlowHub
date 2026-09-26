"""根据源码和已有 App 包版本，计算下一个小修改或功能升级版本。"""

import argparse
import plistlib
import re
from pathlib import Path


def next_version(source: Path, *app_plists: Path, bump: str = "patch") -> str:
    """读取三段数字版本；patch 递增末位，minor 递增中间位并将末位归零。"""
    if bump not in ("patch", "minor"):
        raise ValueError(f"未知的版本升级方式：{bump}")
    versions = []
    for path in (source, *app_plists):
        if path != source and not path.exists():
            continue
        with path.open("rb") as stream:
            value = plistlib.load(stream).get("CFBundleShortVersionString")
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value):
            raise ValueError(f"无效的三段版本号：{path}: {value!r}")
        versions.append(tuple(int(part) for part in value.split(".")))
    major, minor, patch = max(versions)
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bump", choices=("patch", "minor"), default="patch")
    parser.add_argument("source", type=Path)
    parser.add_argument("app_plists", type=Path, nargs="*")
    arguments = parser.parse_args()
    print(next_version(arguments.source, *arguments.app_plists, bump=arguments.bump))
