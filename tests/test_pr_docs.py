import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check-pr-docs.py'


class PrDocsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.policy = {'version': 1, 'required_files': ['README.md'], 'change_rules': [
            {'id': 'module', 'include': ['src/*.py'], 'exclude': ['src/test_*'],
             'documents': ['docs/module.md']}]}
        self.write('.docs-governance.json', json.dumps(self.policy))
        self.write('README.md', '# Project\n[模块](docs/module.md)\n')
        self.write('docs/module.md', '# 模块\n当前说明\n')
        self.write('src/app.py', 'VALUE = 1\n')
        self.write('PROJECT_LOG.md', '## [2026-09-22] init | 初始记录\n')
        self.commit()
        self.base = self.git('rev-parse', 'HEAD').stdout.strip()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def git(self, *args):
        result = subprocess.run(['git', *args], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def scan(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(SCRIPT), '--base', self.base, *args],
                              cwd=cwd or self.root, capture_output=True, text=True)

    def test_code_change_lists_documents_from_subdirectory_and_keeps_index(self):
        self.write('src/app.py', 'VALUE = 2\n')
        self.commit()
        self.write('src/app.py', 'VALUE = 3\n')
        self.git('add', 'src/app.py')
        before = (self.root / '.git/index').read_bytes()
        result = self.scan(cwd=self.root / 'src')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('触发 module', result.stdout)
        self.assertIn('本次未修改，核对是否需要同步', result.stdout)
        self.assertEqual(before, (self.root / '.git/index').read_bytes())

    def test_committed_broken_link_cannot_be_hidden_by_worktree_fix(self):
        self.write('docs/module.md', '# 模块\n[链接](missing.md)\n')
        self.commit()
        self.write('docs/module.md', '# 修好了但没有提交\n')
        result = self.scan()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('missing.md', result.stdout)

    def test_deleted_and_renamed_sources_trigger_old_path_mapping(self):
        self.git('mv', 'src/app.py', 'app.py')
        self.commit()
        result = self.scan()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('触发 module：src/app.py', result.stdout)
        (self.root / 'app.py').unlink()
        self.commit()
        self.assertIn('触发 module', self.scan().stdout)

    def test_missing_mapped_document_blocks_but_excluded_file_does_not_trigger(self):
        self.policy['change_rules'][0]['documents'] = ['docs/unwritten.md']
        self.write('.docs-governance.json', json.dumps(self.policy))
        self.write('src/test_app.py', 'pass\n')
        self.commit()
        self.assertEqual(self.scan().returncode, 0)
        self.write('src/app.py', 'VALUE = 2\n')
        self.commit()
        result = self.scan()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('关联文档缺失', result.stdout)

    def test_original_pr_baseline_catches_history_rewrite_after_second_push(self):
        self.write('PROJECT_LOG.md', '## [2026-09-22] init | 篡改记录\n')
        self.commit()
        self.write('docs/module.md', '# 模块\n补充说明\n')
        self.commit()
        result = self.scan()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('历史有 1 条被删除或改写', result.stdout)

    def test_bad_baseline_and_config_fail_closed_and_no_diff_is_quiet(self):
        self.assertEqual(self.scan().returncode, 0)
        self.assertEqual(self.scan('--base', 'missing-branch').returncode, 2)
        self.policy['change_rules'][0]['documents'] = ['../outside.md']
        self.write('.docs-governance.json', json.dumps(self.policy))
        self.commit()
        self.assertEqual(self.scan().returncode, 2)

    def test_real_push_rejects_invalid_snapshot_then_accepts_fix(self):
        remote = Path(self.temp.name) / 'remote.git'
        self.git('init', '--bare', '-q', str(remote))
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', '-q', 'origin', 'main')
        self.git('symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/main')
        self.git('checkout', '-qb', 'feature')
        hook = self.root / '.git/hooks/pre-push'
        hook.write_text('#!/bin/sh\nexec bash "' + str(ROOT / 'hooks/pre-push.sh') + '" "$@"\n')
        hook.chmod(0o755)
        self.git('config', 'core.hooksPath', str(hook.parent))
        self.write('docs/module.md', '# 模块\n[断链](missing.md)\n')
        self.commit()
        result = subprocess.run(['git', 'push', 'origin', 'feature'], cwd=self.root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing.md', result.stdout + result.stderr)
        result = subprocess.run(['git', '--git-dir', str(remote), 'rev-parse', '--verify', 'refs/heads/feature'],
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.write('docs/module.md', '# 模块\n修复断链\n')
        self.commit()
        self.git('push', '-q', 'origin', 'feature')
        # 更新分支仍检查从目标分支开始的完整 PR 差异。
        self.write('src/app.py', 'VALUE = 3\n')
        self.commit()
        result = self.git('push', 'origin', 'feature')
        self.assertIn('触发 module', result.stdout + result.stderr)

    def test_explicit_head_is_checked_instead_of_checkout_head(self):
        self.write('docs/module.md', '# 模块\n[断链](missing.md)\n')
        self.commit()
        broken = self.git('rev-parse', 'HEAD').stdout.strip()
        self.git('checkout', '--detach', self.base)
        self.assertEqual(self.scan('--head', broken).returncode, 1)

    def test_linked_worktree_uses_shared_objects_without_changing_head(self):
        worktree = Path(self.temp.name) / 'linked'
        self.git('worktree', 'add', '-qb', 'linked', str(worktree))
        (worktree / 'src/app.py').write_text('VALUE = 2\n')
        self.git('-C', str(worktree), 'add', '.')
        self.git('-C', str(worktree), 'commit', '-qm', 'linked change')
        result = self.scan(cwd=worktree)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('触发 module', result.stdout)
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout.strip(), self.base)

    def test_push_event_skips_deletions_but_invalid_input_fails_closed(self):
        def push_event(value):
            return subprocess.run([sys.executable, str(SCRIPT), '--pre-push'],
                                  cwd=self.root, input=value, text=True, capture_output=True)
        self.assertEqual(push_event(f'(delete) {"0" * 40} refs/heads/old {self.base}\n').returncode, 0)
        self.assertEqual(push_event('invalid event\n').returncode, 2)
        # 有待推送分支却没有可解析目标基线，不能静默放行。
        self.assertEqual(push_event(f'refs/heads/main {self.base} refs/heads/main {"0" * 40}\n').returncode, 2)


if __name__ == '__main__':
    unittest.main()
