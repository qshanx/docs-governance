#!/usr/bin/env python3
"""Read project-local verification evidence without executing discovered commands."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from datetime import datetime, timezone

LIMIT = 2 * 1024 * 1024
COMMAND = re.compile(r'(?<![\w/-])(?:bash|sh|python3?|make|npm|pnpm|yarn|pytest|cargo|go)\s+[^`\n]+')
SCRIPT = re.compile(r'(?<![\w/])(?:\./)?(?:[\w.-]+/)+[\w.-]+\.(?:sh|py)\b')
TRIVIAL = re.compile(r'^(?:echo\b.*|printf\b.*|true|false|exit(?:\s+\d+)?|set\s+.*|cd\s+.*|export\s+.*|[A-Za-z_]\w*=.*)$')


def trivial(value):
    return not any(token in value for token in ('&&', '||', ';', '|', '`', '$(')) and bool(TRIVIAL.fullmatch(value))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def redact(text):
    value = r"(?:\"[^\"]*\"|'[^']*'|[^\s;]+)"
    text = re.sub(r'(?i)((?:token|password|secret|api[_-]?key)\s*[=:]\s*)' + value,
                  r'\1[REDACTED]', text)
    text = re.sub(r'(?i)(--?[a-z0-9_-]*(?:token|password|secret|api[_-]?key)(?:\s+|=))' + value,
                  r'\1[REDACTED]', text)
    return re.sub(r'\b(?:sk-|ghp_|github_pat_)[A-Za-z0-9_-]{12,}', '[REDACTED]', text)


class Collector:
    def __init__(self, root):
        self.root = root
        self.files = {}
        self.commands = []
        self.gaps = []
        self.visited = set()

    def gap(self, path, reason):
        item = {'path': str(path), 'reason': reason}
        if item not in self.gaps:
            self.gaps.append(item)

    def read(self, name, required=False):
        path = Path(name)
        if any(part in ('.codex', '.claude', '.agents') for part in path.parts):
            self.gap(name, 'agent_private_directory_out_of_scope'); return None
        if path.is_absolute() or '..' in path.parts:
            self.gap('external', 'outside_project'); return None
        current = self.root
        for part in path.parts:
            current /= part
            if current.is_symlink():
                self.gap(name, 'symlink_not_read'); return None
        if not current.exists():
            if required:
                self.gap(name, 'missing')
            return None
        try:
            if not current.is_file() or current.stat().st_size > LIMIT:
                self.gap(name, 'not_regular_or_over_2MiB'); return None
            raw = current.read_bytes()
            text = raw.decode('utf-8')
        except (OSError, UnicodeError):
            self.gap(name, 'unreadable'); return None
        self.files[str(path)] = {'path': str(path), 'sha256': digest(raw)}
        return text

    def command(self, value, path, line, kind, depth=0):
        value = value.strip().strip('`')
        item = {'source': path, 'line': line, 'kind': kind,
                'command': redact(value), 'status': 'candidate_not_executed', 'scripts': []}
        self.commands.append(item)
        for match in SCRIPT.finditer(value):
            name = match.group()
            prefix = value[:match.start()].rsplit(None, 1)[-1] if value[:match.start()].strip() else ''
            if '$' in prefix or '$' in name or '<' in prefix or '>' in prefix:
                self.gap(path, 'dynamic_command_reference'); continue
            # A regex suffix of an absolute/parent-relative path is not a local reference.
            if re.search(r'(?:/|\.\./)' + re.escape(name), value):
                self.gap(path, 'external_or_parent_command_reference'); continue
            item['scripts'].append(name.removeprefix('./'))
            body = self.read(name, required=True)
            if body is None:
                continue
            if name.endswith('.sh'):
                active = [s.strip() for s in body.splitlines() if s.strip() and not s.lstrip().startswith('#')]
                if not active or all(trivial(s) for s in active):
                    item['status'] = 'hollow_candidate'
                if name not in self.visited and depth < 4:
                    self.visited.add(name)
                    self.scan(body, name, 'script', depth + 1)
                elif depth >= 4:
                    self.gap(name, 'delegation_depth_limit')
        if trivial(value):
            item['status'] = 'hollow_candidate'
        if '$' in value or '<' in value:
            item['dynamic'] = True

    def scan(self, text, path, kind, depth=0):
        for line, value in enumerate(text.splitlines(), 1):
            if value.lstrip().startswith('#'):
                continue
            for match in COMMAND.finditer(value):
                self.command(match.group(), path, line, kind, depth)

    def collect(self):
        for name in ('AGENTS.md', 'CLAUDE.md', 'README.md', 'TESTS.md'):
            text = self.read(name)
            if text is not None:
                self.scan(text, name, 'instruction')
        text = self.read('package.json')
        if text is not None:
            try:
                data = json.loads(text)
                scripts = data.get('scripts', {})
                if not isinstance(scripts, dict):
                    raise ValueError()
                for name, command in scripts.items():
                    if isinstance(command, str) and re.search(r'test|check|verify|lint|build|smoke', name):
                        self.command(command, 'package.json', None, 'package:' + name)
            except (ValueError, AttributeError):
                self.gap('package.json', 'invalid_scripts')
        text = self.read('Makefile')
        if text is not None:
            target = None
            for line, value in enumerate(text.splitlines(), 1):
                match = re.match(r'^([\w.-]+):(?![=])', value)
                if match:
                    target = match.group(1)
                elif value.startswith('\t') and target and re.search(r'test|check|verify|lint|build|smoke', target):
                    self.command(value.strip().lstrip('@'), 'Makefile', line, 'make:' + target)
        ci_dir = self.root / '.github/workflows'
        if (self.root / '.github').is_symlink() or ci_dir.is_symlink():
            self.gap('.github/workflows', 'symlink_not_read')
        elif ci_dir.is_dir():
            for path in sorted(ci_dir.iterdir()):
                if path.suffix not in ('.yml', '.yaml'):
                    continue
                name = path.relative_to(self.root).as_posix()
                text = self.read(name)
                if text is not None:
                    self.scan(text, name, 'ci')
        ci_scripts = {s for c in self.commands if c['kind'] == 'ci' for s in c['scripts']}
        for command in self.commands:
            command['same_literal_script_in_ci'] = bool(set(command['scripts']) & ci_scripts)
        return self


def git_state(root):
    # Git subprocesses load local config includes. Read only bounded local refs;
    # worktree/commondir layouts remain explicitly unsupported, never followed.
    def read(name):
        path = root
        for part in Path(name).parts:
            if part in ('..', '.'):
                raise ValueError()
            path /= part
            if path.is_symlink():
                raise ValueError()
        if not path.is_file() or path.stat().st_size > LIMIT:
            raise ValueError()
        return path.read_text(encoding='utf-8').strip()
    try:
        git_dir = root / '.git'
        if git_dir.is_symlink() or not git_dir.is_dir() or (git_dir / 'commondir').exists():
            raise ValueError()
        head = read('.git/HEAD')
        if head.startswith('ref: '):
            ref = head[5:]
            if not re.fullmatch(r'refs/[A-Za-z0-9_./-]+', ref) or '..' in Path(ref).parts:
                raise ValueError()
            try:
                head = read('.git/' + ref)
            except (OSError, ValueError):
                pairs = [line.split() for line in read('.git/packed-refs').splitlines()]
                head = next(parts[0] for parts in pairs if len(parts) == 2 and parts[1] == ref)
        if not re.fullmatch(r'[0-9a-fA-F]{40}|[0-9a-fA-F]{64}', head):
            raise ValueError()
        return {'status': 'observed', 'head': head, 'dirty': None,
                'dirty_status': 'not_collected_to_avoid_git_filters'}
    except (OSError, UnicodeError, ValueError, StopIteration):
        return {'status': 'unavailable', 'reason': 'no_supported_local_git_refs'}


def collect(root, evidence):
    before = git_state(root)
    collector = Collector(root).collect()
    source_files = sorted(collector.files.values(), key=lambda x: x['path'])
    fingerprint = digest(json.dumps(source_files, sort_keys=True).encode())
    records = []
    for name in evidence:
        text = collector.read(name, required=True)
        if text is None:
            continue
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError()
            records.append({'path': name, 'status': 'unverified',
                            'reason': 'declared_receipt_not_execution_proof',
                            'reported_exit_code': data.get('exit_code') if type(data.get('exit_code')) is int else None,
                            'reported_at': data.get('generated_at') if isinstance(data.get('generated_at'), str) and re.fullmatch(r'[0-9T:+.Z -]{10,40}', data['generated_at']) else None,
                            'execution_environment': 'not_observed',
                            'same_declared_head': bool(before.get('head')) and data.get('head_commit') == before.get('head'),
                            'same_declared_root': data.get('root') == str(root),
                            'reported_status': data.get('status') if data.get('status') in ('pass', 'fail', 'error', 'warning', 'unverified') else 'unknown'})
        except ValueError:
            collector.gap(name, 'expected_json_receipt')
    changed = []
    for info in source_files:
        text = collector.read(info['path'], required=True)
        if text is None or collector.files[info['path']]['sha256'] != info['sha256']:
            changed.append(info['path'])
    after = git_state(root)
    return {'schema_version': 1, 'scope': 'project_worktree', 'root': str(root),
            'generated_at': datetime.now(timezone.utc).isoformat(), 'git': before,
            'collection_changed': bool(changed or before != after), 'changed_files': changed,
            'evidence_fingerprint': fingerprint, 'fingerprint_scope': 'listed_source_files_only',
            'files': source_files, 'commands': collector.commands, 'receipts': records,
            'coverage_gaps': collector.gaps,
            'limitations': ['static_candidates_only', 'ci_conditions_and_execution_not_verified',
                            'no_global_config_or_conversation_history', 'no_discovered_commands_executed',
                            'root_instructions_make_package_github_actions_only', 'no_whole_project_health_verdict']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--evidence', action='append', default=[], help='Explicit project-relative JSON receipt; never executes it')
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('root must be a directory')
        result = collect(root, args.evidence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(json.dumps({'schema_version': 1, 'status': 'error', 'error': type(error).__name__}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
