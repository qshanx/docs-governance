#!/usr/bin/env python3
"""PR 前检查已提交快照；本地 pre-push 与 PR CI 使用同一入口。"""
import argparse
from fnmatch import fnmatchcase
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from docpolicy import read_policy


def git(root, *args, env=None):
    return subprocess.run(['git', *args], cwd=root, env=env, check=True,
                          text=True, capture_output=True).stdout.strip()


def check(root, base, head):
    head = git(root, 'rev-parse', '--verify', '--end-of-options', f'{head}^{{commit}}')
    base = git(root, 'rev-parse', '--verify', '--end-of-options', f'{base}^{{commit}}')
    baseline = git(root, 'merge-base', base, head)
    # 禁用 rename 检测：重命名的旧位置和新位置都要触发映射。
    output = subprocess.run(['git', 'diff', '--no-renames', '--name-only', '-z', baseline, head, '--'],
                            cwd=root, check=True, capture_output=True).stdout
    changed = [os.fsdecode(p) for p in output.split(b'\0') if p]
    print(f'PR 文档检查：{baseline[:12]} → {head[:12]}，变更 {len(changed)} 个文件', flush=True)
    if not changed:
        return 0

    # 独立 index / HEAD，共享只读对象库；不读工作区修复、不改原仓库索引。
    objects = git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'objects')
    env = dict(os.environ)
    for name in git(root, 'rev-parse', '--local-env-vars').splitlines():
        env.pop(name, None)
    env['GIT_OBJECT_DIRECTORY'] = objects
    with tempfile.TemporaryDirectory(prefix='pr-docs-') as directory:
        snapshot = Path(directory).resolve()
        git(snapshot, 'init', '--quiet', '--template=', env=env)
        git(snapshot, 'config', 'core.hooksPath', str(snapshot / '.git/hooks'), env=env)
        git(snapshot, 'update-ref', 'HEAD', head, env=env)
        git(snapshot, 'read-tree', head, env=env)
        git(snapshot, 'checkout-index', '--all', env=env)
        policy = read_policy(snapshot) or {}
        missing = False
        for rule in policy.get('change_rules', []):
            hits = [p for p in changed if any(fnmatchcase(p, pat) for pat in rule['include'])
                    and not any(fnmatchcase(p, pat) for pat in rule.get('exclude', []))]
            if not hits:
                continue
            print(f'触发 {rule["id"]}：{", ".join(hits)}', flush=True)
            for name in rule['documents']:
                path = snapshot / name
                if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(snapshot):
                    print(f'阻断：关联文档缺失或不是仓库内普通文件：{name}', flush=True)
                    missing = True
                else:
                    status = '本次已修改，核对内容' if name in changed else '本次未修改，核对是否需要同步'
                    print(f'  语义审查：{name}（{status}）', flush=True)
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('audit-docs.py')),
                                 '--root', str(snapshot), '--scope', 'full', '--base-ref', baseline],
                                env=env, check=False, timeout=60)
        if result.returncode:
            return 1 if result.returncode == 1 else 2
        if missing:
            return 1
    print('PR 确定性扫描通过；关联文档的业务含义与同步必要性仍须审查。', flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--base', help='PR 目标分支或提交；必须本地可解析')
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--pre-push', action='store_true')
    parser.add_argument('--remote', default='origin')
    args = parser.parse_args()
    try:
        root = Path(git(args.root, 'rev-parse', '--show-toplevel'))
        if args.pre_push:
            heads = []
            for line in sys.stdin:
                fields = line.split()
                if len(fields) != 4:
                    raise ValueError('pre-push 输入必须包含四列')
                _, sha, remote_ref, _ = fields
                if remote_ref.startswith('refs/heads/') and set(sha) != {'0'}:
                    heads.append(sha)
            if not heads:
                return 0  # 删除分支及 tag 不会产生 PR 分支变更。
            base = args.base or os.environ.get('DOCS_GOVERNANCE_PR_BASE')
            if not base:
                base = git(root, 'symbolic-ref', f'refs/remotes/{args.remote}/HEAD')
            for head in dict.fromkeys(heads):
                code = check(root, base, head)
                if code:
                    return code
            return 0
        if not args.base:
            raise ValueError('必须用 --base 指定 PR 目标分支')
        return check(root, args.base, args.head)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'PR 文档检查未完成，阻止继续：{exc}\n请核对基线；pre-push 可设置 DOCS_GOVERNANCE_PR_BASE。', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
