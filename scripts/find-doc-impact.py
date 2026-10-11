#!/usr/bin/env python3
"""只读检索变更涉及的 Markdown 候选；不判定正文是否过期。"""
import argparse
import difflib
from fnmatch import fnmatchcase
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

LIMIT = 2 * 1024 * 1024
DOC_SUFFIXES = {'.md', '.mdx', '.markdown'}
WORDS = re.compile(r'[A-Za-z_][A-Za-z_0-9]{2,}|[\u4e00-\u9fff]{2,}')
STOP = set('def class return import from if else elif for while with as true false null None '
           'self const let var function async await export default type object string integer '
           'number boolean properties required additionalProperties minimum maximum json dict'.split())


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True).stdout


def tree(root, ref):
    result = {}
    for record in git(root, 'ls-tree', '-rz', ref).split(b'\0'):
        if record:
            meta, name = record.split(b'\t', 1)
            mode, _, oid = meta.decode().split()
            result[name.decode()] = (mode, oid)
    return result


def scan(root, base, head=None, worktree=False, terms=()):
    root = Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    resolve = lambda ref: git(root, 'rev-parse', '--verify', '--end-of-options',
                              f'{ref}^{{commit}}').decode().strip()
    base = resolve(base)
    head = resolve(head or 'HEAD')
    baseline = base if worktree else git(root, 'merge-base', base, head).decode().strip()
    old_tree = tree(root, baseline)
    new_tree = tree(root, head)
    if worktree:
        names = git(root, 'ls-files', '-co', '--exclude-standard', '-z').decode().split('\0')
        new_tree = {name: None for name in names if name and
                    ((root / name).exists() or (root / name).is_symlink())}
    skipped, hashes = [], {}

    def read(name, entries, current=False):
        if name not in entries:
            return ''
        label = 'current' if current else 'baseline'
        if current and worktree:
            path = root / name
            if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
                skipped.append({'path': name, 'scope': label, 'reason': 'not regular file'})
                return None
            if path.stat().st_size > LIMIT:
                skipped.append({'path': name, 'scope': label, 'reason': 'over 2 MiB'})
                return None
            raw = path.read_bytes()
            hashes[name] = hashlib.sha256(raw).hexdigest()
        else:
            mode, oid = entries[name]
            if mode not in ('100644', '100755'):
                skipped.append({'path': name, 'scope': label, 'reason': 'not regular blob'})
                return None
            if int(git(root, 'cat-file', '-s', oid)) > LIMIT:
                skipped.append({'path': name, 'scope': label, 'reason': 'over 2 MiB'})
                return None
            raw = git(root, 'cat-file', 'blob', oid)
        try:
            if b'\0' in raw:
                raise UnicodeError()
            return raw.decode('utf-8')
        except UnicodeError:
            skipped.append({'path': name, 'scope': label, 'reason': 'non UTF-8 text'})
            return None

    if worktree:
        tracked = git(root, 'diff', '--no-ext-diff', '--no-renames', '--name-only', '-z', baseline, '--')
        untracked = git(root, 'ls-files', '--others', '--exclude-standard', '-z')
        changed = sorted(set(p for p in (tracked + untracked).decode().split('\0') if p))
    else:
        changed = sorted(name for name in set(old_tree) | set(new_tree)
                         if old_tree.get(name) != new_tree.get(name))
    current = {}
    diffs = {}
    actual = []
    for name in changed:
        old = read(name, old_tree)
        new = read(name, new_tree, True)
        current[name] = new
        if old is not None and new is not None and old == new:
            continue
        actual.append(name)
        if Path(name).suffix.lower() not in DOC_SUFFIXES and old is not None and new is not None:
            diffs[name] = list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3))

    # 只从变更行提取词，并补充周围函数／类型声明。它们是搜索线索，不是事实结论。
    hints = {}
    for name, diff in diffs.items():
        removed, added, declarations = set(), set(), set()
        for line in diff[2:]:
            if line.startswith('-'):
                removed.update(WORDS.findall(line[1:]))
            elif line.startswith('+'):
                added.update(WORDS.findall(line[1:]))
            declaration = re.match(r'[-+ ]\s*(?:async )?(?:def|class|function)\s+(\w+)', line)
            if declaration:
                declarations.add(declaration[1])
        for term in (removed ^ added) | declarations:
            if term not in STOP and not re.fullmatch(r'[a-fA-F0-9]{16,}', term):
                hints.setdefault(term, set()).add(name)
    for term in terms:
        if not term.strip():
            raise ValueError('--term 不能为空')
        hints.setdefault(term, set()).add('explicit-term')
    policy_text = current.get('.docs-governance.json')
    if '.docs-governance.json' not in current:
        policy_text = read('.docs-governance.json', new_tree, True)
    if policy_text is None:
        raise ValueError('无法读取当前版本的 .docs-governance.json')
    policy = json.loads(policy_text) if policy_text else {}
    mapped = {}
    for rule in policy.get('change_rules', []):
        hits = [p for p in actual if any(fnmatchcase(p, pat) for pat in rule['include'])
                and not any(fnmatchcase(p, pat) for pat in rule.get('exclude', []))]
        if hits:
            for name in rule['documents']:
                mapped.setdefault(name, []).append({'kind': 'mapping', 'rule': rule['id'], 'sources': hits})

    candidates = []
    docs = sorted(p for p in new_tree if Path(p).suffix.lower() in DOC_SUFFIXES)
    patterns = {term: re.compile(r'(?<![\w])' + re.escape(term) + r'(?![\w])')
                if term.isascii() else re.compile(re.escape(term)) for term in hints}
    for name in sorted(set(docs) | set(mapped)):
        body = current[name] if name in current else read(name, new_tree, True)
        reasons = list(mapped.get(name, []))
        matches = []
        heading = ''
        for number, line in enumerate((body or '').splitlines(), 1):
            if line.startswith('#'):
                heading = line.lstrip('#').strip()
            found = [{'kind': 'term', 'term': term, 'sources': sorted(hints[term])}
                     for term, pattern in patterns.items() if pattern.search(line)]
            # 相对 Markdown 链接按文档所在目录解析；兼顾正文中的仓库路径。
            targets = re.findall(r'\]\(<?([^\s)>]+)', line)
            paths = set()
            for target in targets:
                url = urlsplit(target)
                if not url.scheme and url.path:
                    paths.add(posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))))
            for source in actual:
                if source in paths or source in line:
                    found.append({'kind': 'reference', 'source': source})
            if found:
                matches.append({'line': number, 'heading': heading, 'text': line, 'reasons': found})
        if matches or reasons:
            candidates.append({'path': name, 'status': 'candidate', 'exists': name in new_tree,
                               'reasons': reasons, 'matches': matches})
    return {'baseline': baseline, 'head': head, 'mode': 'worktree' if worktree else 'committed',
            'changed_files': actual, 'search_terms': {k: sorted(v) for k, v in sorted(hints.items())},
            'documents_scanned': len(docs), 'skipped': skipped, 'worktree_sha256': hashes,
            'candidates': candidates,
            'limitations': ['候选不是过期结论；历史、同名词和内部重构须判读。',
                            '仅检索本地 Git 文件中的 Markdown；无命中不证明无影响。',
                            '功能含义与同义表达由 Agent 补充 --term 并沿引用核对。']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--base', required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--head', help='受检提交，默认 HEAD；忽略工作区修改')
    mode.add_argument('--worktree', action='store_true', help='指定 base 与当前文件比较，含非忽略的未跟踪文件')
    parser.add_argument('--term', action='append', default=[], help='补充功能名、旧名称等搜索词，可重复')
    args = parser.parse_args()
    try:
        result = scan(args.root, args.base, args.head, args.worktree, args.term)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'候选检索未完成：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
