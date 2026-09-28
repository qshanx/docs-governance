import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentPolicyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.policy = {'version': 1, 'required_files': ['docs/product/README.md'],
                       'placement': [{'id': 'prd', 'include': ['*.md'], 'exclude': ['templates/*'],
                                      'heading_keywords': ['PRD'], 'allowed_dirs': ['docs/product']}],
                       'auto_audit': {'on_stop': True}}
        self.write('docs/product/README.md', '# 产品入口\n')
        self.save_policy()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def save_policy(self):
        self.write('.docs-governance.json', json.dumps(self.policy))

    def command(self, *args):
        return subprocess.run(args, cwd=self.root, text=True, capture_output=True)

    def audit(self):
        return self.command(sys.executable, str(ROOT / 'scripts/audit-docs.py'), '--scope', 'artifacts', '--format', 'json')

    def test_heading_enforced_but_mentions_fences_and_exceptions_allowed(self):
        self.write('notes.md', '# 阅读\n提到了 PRD\n```md\n# PRD\n```\n')
        self.write('templates/prd.md', '# PRD 模板\n')
        self.write('docs/product/prd.md', '# PRD\n')
        self.assertEqual(self.audit().returncode, 0)
        self.write('wrong.md', '# PRD 错放\n')
        result = self.audit()
        self.assertEqual(result.returncode, 1)
        finding = next(x for x in json.loads(result.stdout)['findings'] if x['check'] == 'policy.placement')
        self.assertEqual(finding['path'], 'wrong.md')
        self.assertEqual(finding['evidence']['rule'], 'prd')

    def test_required_missing_and_directory_are_failures(self):
        path = self.root / 'docs/product/README.md'
        path.unlink()
        self.assertEqual(self.audit().returncode, 1)
        path.mkdir()
        self.assertEqual(self.audit().returncode, 1)

    def test_directory_prefix_is_not_allowed_sibling(self):
        self.write('docs/product-other/prd.md', '# PRD\n')
        self.assertEqual(self.audit().returncode, 1)

    def test_bad_policy_is_error_not_silent_pass(self):
        for change in ({'version': 2}, {'placement': {}}, {'auto_audit': {'on_stop': 'yes'}},
                       {'required_files': ['../outside.md']}, {'typo': True},
                       {'change_rules': {}}, {'change_rules': [{'id': 'x', 'include': [], 'documents': ['a.md']}]},
                       {'change_rules': [{'id': 'x', 'include': ['src/*'], 'documents': ['*.md']}]},
                       {'change_rules': [{'id': 'x', 'include': ['src/*'], 'documents': ['a.md'], 'command': 'echo'}]}):
            with self.subTest(change=change):
                self.write('.docs-governance.json', json.dumps({**self.policy, **change}))
                self.assertEqual(self.audit().returncode, 2)
        self.write('.docs-governance.json', '{broken')
        self.assertEqual(self.audit().returncode, 2)

    def test_no_policy_is_optional(self):
        (self.root / '.docs-governance.json').unlink()
        self.write('other.md', '# PRD\n')
        self.assertEqual(self.audit().returncode, 0)

    def test_script_location_with_explicit_test_exception(self):
        self.policy['placement'] = [{'id': 'scripts', 'include': ['*.py', '*.sh'],
                                     'exclude': ['tests/fixtures/*'], 'allowed_dirs': ['scripts', 'hooks']}]
        self.save_policy()
        self.write('scripts/check.py', 'pass\n')
        self.write('tests/fixtures/fake.sh', '#!/bin/sh\n')
        self.assertEqual(self.audit().returncode, 0)
        self.write('misc/check.py', 'pass\n')
        self.assertEqual(self.audit().returncode, 1)

    def test_symlink_cannot_satisfy_required_file(self):
        (self.root / 'docs/product/README.md').unlink()
        self.write('real.md', '# 产品入口\n')
        (self.root / 'docs/product/README.md').symlink_to(self.root / 'real.md')
        self.assertEqual(self.audit().returncode, 1)

    def test_staged_snapshot_not_hidden_by_unstaged_fix(self):
        self.assertEqual(self.command('git', 'init', '-q').returncode, 0)
        self.write('wrong.md', '# PRD\n')
        self.assertEqual(self.command('git', 'add', '.').returncode, 0)
        self.write('wrong.md', '# 普通说明\n')
        self.assertEqual(self.audit().returncode, 0)
        result = self.command(sys.executable, str(ROOT / 'scripts/check-staged-docs.py'))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.command('git', 'add', 'wrong.md').returncode, 0)
        result = self.command(sys.executable, str(ROOT / 'scripts/check-staged-docs.py'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_stop_changes_trigger_cache_and_unchanged_success_is_quiet(self):
        def stop():
            return self.command('bash', str(ROOT / 'hooks/check-on-stop.sh'))
        first = stop()
        self.assertEqual(first.returncode, 0)
        state = self.root / '.governance/auto-audit.json'
        before = state.read_bytes()
        self.assertIn('确定性检查通过', first.stderr)
        second = stop()
        self.assertEqual(second.stderr, '')
        self.assertEqual(before, state.read_bytes())
        self.write('wrong.md', '# PRD\n')
        bad = stop()
        self.assertEqual(bad.returncode, 0)
        self.assertIn('wrong.md', bad.stderr)
        self.assertEqual(json.loads(state.read_text())['report']['exit_code'], 1)
        (self.root / 'wrong.md').unlink()
        self.assertIn('确定性检查通过', stop().stderr)

    def test_stop_reports_bad_policy_and_does_not_block(self):
        self.write('.docs-governance.json', '{}')
        result = self.command('bash', str(ROOT / 'hooks/check-on-stop.sh'))
        self.assertEqual(result.returncode, 0)
        self.assertIn('未完成', result.stderr)

    def test_precommit_wrapper_rejects_wrong_location(self):
        self.assertEqual(self.command('git', 'init', '-q').returncode, 0)
        self.write('wrong.md', '# PRD\n')
        self.assertEqual(self.command('git', 'add', '.').returncode, 0)
        result = self.command('bash', str(ROOT / 'hooks/pre-commit.sh'))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.write('wrong.md', '# 普通文档\n')
        self.assertEqual(self.command('git', 'add', 'wrong.md').returncode, 0)
        self.assertEqual(self.command('bash', str(ROOT / 'hooks/pre-commit.sh')).returncode, 0)

    def test_stop_does_not_write_through_cache_symlink(self):
        with tempfile.TemporaryDirectory() as external:
            (self.root / '.governance').symlink_to(external, target_is_directory=True)
            result = self.command('bash', str(ROOT / 'hooks/check-on-stop.sh'))
            self.assertEqual(result.returncode, 0)
            self.assertIn('缓存路径不能为软链接', result.stderr)
            self.assertEqual(list(Path(external).iterdir()), [])

    def test_legacy_stop_without_policy_still_nonblocking(self):
        (self.root / '.docs-governance.json').unlink()
        self.assertIn('无法确定治理根', self.command('bash', str(ROOT / 'hooks/check-on-stop.sh')).stderr)
        self.write('PROJECT_LOG.md', '## [2020-01-01] docs | 修改文件\n昨天改了文件\n')
        result = self.command('bash', str(ROOT / 'hooks/check-on-stop.sh'))
        self.assertEqual(result.returncode, 0)
        self.assertIn('相对时间', result.stderr)

    def stop_from(self, directory, explicit=None):
        env = {k: v for k, v in os.environ.items() if k != 'DOCS_GOVERNANCE_ROOT'}
        if explicit is not None:
            env['DOCS_GOVERNANCE_ROOT'] = str(explicit)
        return subprocess.run(['bash', str(ROOT / 'hooks/check-on-stop.sh')],
                              cwd=directory, env=env, text=True, capture_output=True)

    def test_stop_same_config_and_cache_from_root_and_deep_directories(self):
        self.command('git', 'init', '-q')
        self.write('wrong.md', '# PRD 错放\n')
        deep = self.root / 'src/a/b'
        deep.mkdir(parents=True)
        results = [self.stop_from(p) for p in (self.root, self.root / 'src', deep)]
        for result in results:
            self.assertEqual(result.returncode, 0)
            self.assertIn('wrong.md', result.stderr)
        self.assertEqual(len({r.stderr for r in results}), 1)
        self.assertTrue((self.root / '.governance/auto-audit.json').is_file())
        self.assertFalse((deep / '.governance').exists())

    def test_stop_nearest_subproject_policy_wins_and_can_disable_stop(self):
        self.command('git', 'init', '-q')
        child = self.root / 'apps/web'
        deep = child / 'src/deep'
        deep.mkdir(parents=True)
        self.policy['required_files'] = ['missing-parent.md']
        self.save_policy()
        self.write('apps/web/.docs-governance.json', json.dumps({
            'version': 1, 'required_files': ['missing-child.md'], 'auto_audit': {'on_stop': True}}))
        result = self.stop_from(deep)
        self.assertIn('missing-child.md', result.stderr)
        self.assertNotIn('missing-parent.md', result.stderr)
        self.assertFalse((self.root / '.governance').exists())
        self.assertTrue((child / '.governance/auto-audit.json').exists())
        self.write('apps/web/.docs-governance.json', '{"version":1,"auto_audit":{"on_stop":false}}')
        self.assertEqual(self.stop_from(deep).stderr, '')

    def test_stop_explicit_root_overrides_child_but_invalid_root_never_falls_back(self):
        deep = self.root / 'apps/web/src'
        deep.mkdir(parents=True)
        self.write('apps/web/.docs-governance.json', '{"version":1,"auto_audit":{"on_stop":false}}')
        self.write('wrong.md', '# PRD\n')
        self.assertIn('wrong.md', self.stop_from(deep, self.root).stderr)
        for explicit in (self.root / 'not-created', deep):
            result = self.stop_from(deep, explicit)
            self.assertEqual(result.returncode, 0)
            self.assertIn('显式治理根', result.stderr)
            self.assertNotIn('wrong.md', result.stderr)
        self.assertFalse((deep / '.governance').exists())

    def test_stop_nested_git_repository_does_not_inherit_parent_policy(self):
        self.command('git', 'init', '-q')
        nested = self.root / 'nested'
        nested.mkdir()
        self.command('git', '-C', str(nested), 'init', '-q')
        result = self.stop_from(nested)
        self.assertEqual(result.returncode, 0)
        self.assertIn('无法确定治理根', result.stderr)
        self.assertFalse((self.root / '.governance').exists())
        self.assertFalse((nested / '.governance').exists())

    def test_stop_non_git_and_legacy_projects_resolve_ancestors(self):
        deep = self.root / 'src/deep'
        deep.mkdir(parents=True)
        self.write('wrong.md', '# PRD\n')
        self.assertIn('wrong.md', self.stop_from(deep).stderr)
        (self.root / '.docs-governance.json').unlink()
        self.write('PROJECT_LOG.md', '## [2020-01-01] docs | 更新\n昨天更新\n')
        self.assertIn('相对时间', self.stop_from(deep).stderr)
        self.command('git', 'init', '-q')
        self.write('src/CLAUDE.md', '# 模块规则，不是独立治理根\n')
        self.assertIn('相对时间', self.stop_from(deep).stderr)

    def test_auto_audit_direct_cli_uses_same_root_resolution(self):
        self.write('wrong.md', '# PRD\n')
        deep = self.root / 'src'
        deep.mkdir()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/auto-audit.py')],
                                cwd=deep, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('wrong.md', result.stderr)
        result = self.command(sys.executable, str(ROOT / 'scripts/auto-audit.py'),
                              '--root', str(self.root / 'missing'))
        self.assertEqual(result.returncode, 2)

    def test_stop_broken_nearest_policy_reports_error_without_parent_fallback(self):
        deep = self.root / 'app/src'
        deep.mkdir(parents=True)
        self.write('app/.docs-governance.json', '{broken')
        result = self.stop_from(deep)
        self.assertEqual(result.returncode, 0)
        self.assertIn('未完成', result.stderr)
        self.assertFalse((self.root / '.governance').exists())
        config = self.root / 'app/.docs-governance.json'
        config.unlink()
        config.mkdir()
        self.assertIn('未完成', self.stop_from(deep).stderr)
        config.rmdir()
        config.symlink_to('missing-policy.json')
        self.assertIn('规则文件不能是软链接', self.stop_from(deep).stderr)

    def test_stop_linked_worktree_selects_its_own_root(self):
        self.command('git', 'init', '-q')
        self.command('git', 'add', '.')
        result = self.command('git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                              '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            linked = Path(directory) / 'linked'
            result = self.command('git', 'worktree', 'add', '--detach', str(linked), 'HEAD')
            self.assertEqual(result.returncode, 0, result.stderr)
            try:
                (linked / 'wrong.md').write_text('# PRD\n')
                (linked / 'src').mkdir()
                self.assertIn('wrong.md', self.stop_from(linked / 'src').stderr)
                self.assertTrue((linked / '.governance/auto-audit.json').exists())
                self.assertFalse((self.root / '.governance').exists())
            finally:
                self.command('git', 'worktree', 'remove', '--force', str(linked))


if __name__ == '__main__':
    unittest.main()
