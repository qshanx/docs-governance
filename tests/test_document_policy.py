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
        self.assertEqual(self.command('bash', str(ROOT / 'hooks/check-on-stop.sh')).stderr, '')
        self.write('PROJECT_LOG.md', '## [2020-01-01] docs | 修改文件\n昨天改了文件\n')
        result = self.command('bash', str(ROOT / 'hooks/check-on-stop.sh'))
        self.assertEqual(result.returncode, 0)
        self.assertIn('相对时间', result.stderr)


if __name__ == '__main__':
    unittest.main()
