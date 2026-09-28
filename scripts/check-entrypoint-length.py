#!/usr/bin/env python3
"""只读检查指定入口文件：0 通过，1 超过 200 行，2 参数或读取错误。"""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description="检查每份 Agent 入口是否不超过 200 行")
    parser.add_argument("files", nargs="+", type=Path, help="本次受检入口文件")
    args = parser.parse_args()
    status = 0
    for path in args.files:
        try:
            with path.open(encoding="utf-8") as source:
                count = sum(1 for _ in source)
        except (OSError, UnicodeError) as error:
            print(f"无法检查 {path}: {error}", file=sys.stderr)
            status = 2
            continue
        print(f"{'通过' if count <= 200 else '超限'}: {path} ({count}/200 行)")
        if count > 200:
            status = max(status, 1)
    return status


if __name__ == "__main__":
    sys.exit(main())
