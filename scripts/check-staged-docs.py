#!/usr/bin/env python3
"""检查暂存区快照，防止工作区的未暂存修复掩盖提交中的文档问题。"""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        repo = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=args.root,
                              text=True, capture_output=True, check=True).stdout.strip()
        with tempfile.TemporaryDirectory(prefix='staged-docs-') as temp:
            subprocess.run(['git', 'checkout-index', '--all', '--prefix', temp + '/'], cwd=repo,
                           capture_output=True, text=True, check=True)
            return subprocess.run([sys.executable, str(Path(__file__).with_name('audit-docs.py')),
                                   '--root', temp, '--scope', 'artifacts'], check=False).returncode
    except (OSError, subprocess.SubprocessError) as exc:
        print(f'暂存文档审计未完成：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
