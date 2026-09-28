#!/usr/bin/env python3
"""将推送检查固定在 Git 元数据中，避免切分支使已装 hook 失效。"""
import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile


RUNTIME_FILES = ('check-pr-docs.py', 'audit-docs.py', 'docpolicy.py', 'logformat.py')


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def install(root, replace=False):
    root = Path(git(root, 'rev-parse', '--show-toplevel')).resolve()
    common = Path(git(root, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
    hook = Path(git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'hooks/pre-push'))
    if hook.is_symlink():
        raise ValueError('现有 hook 是软链接，请先人工核对，不自动替换')
    hook = hook.resolve()
    if hook.is_relative_to(root) and not hook.is_relative_to(common):
        raise ValueError('core.hooksPath 位于工作树内；请先明确稳定安装位置，不自动改 Git 配置')
    if hook.exists() and (not hook.is_file() or not replace):
        raise ValueError('已有 hook，未修改；确认替换范围后才可用 --replace（先备份）')
    # 先读全所有依赖，缺文件时不碰现有安装。
    source = Path(__file__).resolve().parent
    payload = {name: (source / name).read_bytes() for name in RUNTIME_FILES}
    storage = common / 'docs-governance'
    if storage.is_symlink():
        raise ValueError('稳定运行目录不能为软链接')
    storage.mkdir(exist_ok=True)
    runtime = Path(tempfile.mkdtemp(prefix='pre-push-', dir=storage))
    for name, content in payload.items():
        (runtime / name).write_bytes(content)
    hook.parent.mkdir(parents=True, exist_ok=True)
    if hook.exists():
        with tempfile.NamedTemporaryFile(prefix='pre-push-backup-', dir=storage, delete=False) as backup:
            backup_path = Path(backup.name)
        shutil.copy2(hook, backup_path)
        print(f'原 hook 备份：{backup_path}')
    script = '#!/bin/sh\n# docs-governance: stable pre-push snapshot\n'
    script += ('exec python3 ' + shlex.quote(str(runtime / 'check-pr-docs.py'))
               + ' --pre-push --remote "${1:-origin}"\n')
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', prefix='.pre-push-',
                                     dir=hook.parent, delete=False) as staged:
        staged.write(script)
        staged_path = Path(staged.name)
    staged_path.chmod(0o755)
    os.replace(staged_path, hook)
    print(f'已安装：{hook}\n运行快照：{runtime}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--replace', action='store_true', help='明确批准替换已有 hook；原文件先备份')
    args = parser.parse_args()
    try:
        install(args.root, args.replace)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(2, f'pre-push 安装未完成：{exc}\n')


if __name__ == '__main__':
    main()
