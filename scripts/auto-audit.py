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

from docpolicy import POLICY_NAME, files_under, read_policy

SPINE = ('CLAUDE.md', 'CLAUDE_MAP.md', 'PROJECT_STATUS.md', 'PROJECT_LOG.md')


def governance_root(start, explicit=None):
    """显式根优先；否则在当前 Git 边界内找最近配置，再回退旧四件套。"""
    def has_policy(path):
        config = path / POLICY_NAME
        return config.exists() or config.is_symlink()

    def has_spine(path):
        return any((path / name).is_file() for name in SPINE)

    if explicit is not None:
        root = Path(explicit).resolve()
        if not str(explicit).strip() or not root.is_dir() or not (has_policy(root) or has_spine(root)):
            raise ValueError(f'显式治理根无效或没有治理配置／四件套：{explicit}')
        return root

    start = start.resolve()
    repository = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=start,
                                text=True, capture_output=True, env={**os.environ, 'LC_ALL': 'C'})
    boundary = None
    if repository.returncode == 0:
        boundary = Path(repository.stdout.strip()).resolve()
        if not start.is_relative_to(boundary):
            raise ValueError('当前目录不在 Git 返回的根目录中，请设置 DOCS_GOVERNANCE_ROOT')
    elif not repository.stderr.startswith('fatal: not a git repository (or any'):
        raise ValueError(f'Git 根定位失败：{repository.stderr.strip()}')

    ancestors = []
    for candidate in (start, *start.parents):
        ancestors.append(candidate)
        if has_policy(candidate):
            return candidate
        if candidate == boundary:
            break
    # Git 项目的模块级 CLAUDE.md 不是独立治理根；子项目须显式配置。
    legacy = [boundary] if boundary is not None else ancestors
    for candidate in legacy:
        if has_spine(candidate):
            return candidate
    raise ValueError('无法确定治理根：未找到 .docs-governance.json 或治理四件套；'
                     '请检查项目配置或设置 DOCS_GOVERNANCE_ROOT，本次未执行审计')


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
    parser.add_argument('--root', type=Path, help='显式治理根；未指定时读取 DOCS_GOVERNANCE_ROOT 或自动定位')
    parser.add_argument('--resolve-root', action='store_true', help='只输出治理根，供 Stop 兼容旧四件套提醒')
    args = parser.parse_args()
    try:
        explicit = args.root if args.root is not None else os.environ.get('DOCS_GOVERNANCE_ROOT')
        root = governance_root(Path.cwd(), explicit)
        if args.resolve_root:
            print(root)
            return 0
        return run(root)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'docs-governance 自动审计未完成：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
