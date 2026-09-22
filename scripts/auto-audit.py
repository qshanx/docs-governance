#!/usr/bin/env python3
"""Stop 事件按内容变化运行，不创建定时任务。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from docpolicy import files_under, read_policy


def run(root):
    policy = read_policy(root)
    if policy is None or not policy.get('auto_audit', {}).get('on_stop', False):
        return 0
    digest = hashlib.sha256()
    for tool in ('auto-audit.py', 'audit-docs.py', 'docpolicy.py', 'logformat.py'):
        digest.update(Path(__file__).with_name(tool).read_bytes())
    for path in sorted(files_under(root)):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b'\0')
        if path.is_symlink():
            digest.update(os.readlink(path).encode())
        else:
            with path.open('rb') as handle:
                for chunk in iter(lambda: handle.read(65536), b''):
                    digest.update(chunk)
        digest.update(b'\0')
    head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=root, text=True, capture_output=True)
    digest.update(head.stdout.encode())
    fingerprint = digest.hexdigest()
    directory = root / '.governance'
    state = directory / 'auto-audit.json'
    if directory.is_symlink() or state.is_symlink():
        raise ValueError('审计缓存路径不能为软链接')
    cached = None
    try:
        cached = json.loads(state.read_text())
    except (FileNotFoundError, ValueError):
        pass
    now = time.time()
    reusable = (isinstance(cached, dict) and cached.get('fingerprint') == fingerprint
                and isinstance(cached.get('report'), dict)
                and cached['report'].get('exit_code') in (0, 1, 2)
                and isinstance(cached['report'].get('findings'), list))
    if reusable:
        report = cached['report']
    else:
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('audit-docs.py')),
                                 '--root', str(root), '--scope', 'full', '--format', 'json'],
                                text=True, capture_output=True, timeout=45)
        report = json.loads(result.stdout)
        if report.get('exit_code') != result.returncode:
            raise ValueError('审计退出码与报告不一致')
        directory.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', dir=directory, delete=False, encoding='utf-8') as handle:
            json.dump({'fingerprint': fingerprint, 'checked_at': now, 'report': report}, handle, ensure_ascii=False)
            temp_path = handle.name
        os.replace(temp_path, state)
    if report.get('exit_code'):
        print('docs-governance 自动审计：发现问题；未修改文档。', file=sys.stderr)
        for item in report.get('findings', []):
            if item['status'] in ('error', 'fail'):
                print(item['message'], file=sys.stderr)
    elif not reusable:
        print('docs-governance 自动审计：确定性检查通过；语义判断仍需文档审查。', file=sys.stderr)
    return report.get('exit_code', 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        return run(args.root.resolve())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'docs-governance 自动审计未完成：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
