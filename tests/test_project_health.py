from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/collect-project-health.py'


class ProjectHealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        self.root.mkdir()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run_health(self, *args):
        proc = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), *args],
                              capture_output=True, text=True, timeout=20)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        return json.loads(proc.stdout)

    def test_script_entrypoint_and_ci_without_makefile(self):
        self.write('CLAUDE.md', '运行 `bash scripts/verify.sh`\n')
        self.write('scripts/verify.sh', 'python3 -m unittest discover -s tests\n')
        self.write('.github/workflows/verify.yml', 'jobs:\n  check:\n    steps:\n      - run: bash scripts/verify.sh\n')
        data = self.run_health()
        command = next(c for c in data['commands'] if c['kind'] == 'instruction')
        self.assertTrue(command['same_literal_script_in_ci'])
        self.assertEqual(data['coverage_gaps'], [])
        self.assertNotIn('pass', [c['status'] for c in data['commands']])

    def test_hollow_script_not_executed(self):
        self.write('AGENTS.md', '`bash scripts/verify.sh`\n')
        self.write('scripts/verify.sh', 'echo success\nexit 0\n')
        self.write('package.json', json.dumps({'scripts': {'test': 'touch SHOULD_NOT_EXIST'}}))
        data = self.run_health()
        self.assertEqual(data['commands'][0]['status'], 'hollow_candidate')
        self.assertFalse((self.root / 'SHOULD_NOT_EXIST').exists())

    def test_external_symlinks_and_evidence_not_read(self):
        outside = self.root.parent / 'outside'
        outside.write_text('private marker')
        (self.root / 'AGENTS.md').symlink_to(outside)
        (self.root / '.github').symlink_to(self.root.parent)
        data = self.run_health('--evidence', '../outside')
        self.assertEqual(data['files'], [])
        self.assertNotIn('private marker', json.dumps(data))
        self.assertIn('outside_project', [g['reason'] for g in data['coverage_gaps']])

    def test_receipt_is_not_current_pass_and_history_not_scanned(self):
        self.write('old.json', json.dumps({'status': 'pass', 'root': '/old/project', 'head_commit': 'old'}))
        self.write('.codex/sessions/history.json', 'private marker')
        data = self.run_health('--evidence', 'old.json')
        self.assertEqual(data['receipts'][0]['status'], 'unverified')
        self.assertFalse(data['receipts'][0]['same_declared_root'])
        self.assertNotIn('private marker', json.dumps(data))
        self.assertEqual(data['files'], [])

    def test_source_changes_invalidate_evidence_fingerprint(self):
        self.write('TESTS.md', '`python3 -m unittest discover`\n')
        first = self.run_health()
        self.write('TESTS.md', '`python3 -m unittest discover -s tests`\n')
        second = self.run_health()
        self.assertNotEqual(first['evidence_fingerprint'], second['evidence_fingerprint'])

    def test_missing_script_and_invalid_receipt_are_gaps(self):
        self.write('README.md', '`bash scripts/missing.sh`\n')
        self.write('log.txt', 'all tests passed')
        data = self.run_health('--evidence', 'log.txt')
        self.assertEqual({g['reason'] for g in data['coverage_gaps']}, {'missing', 'expected_json_receipt'})

    def test_plain_package_and_make_commands_collected(self):
        self.write('package.json', json.dumps({'scripts': {'test': 'echo success', 'start': 'node app.js'}}))
        self.write('Makefile', 'verify:\n\tpython3 -m unittest\n')
        data = self.run_health()
        self.assertEqual({c['kind'] for c in data['commands']}, {'package:test', 'make:verify'})
        self.assertEqual(next(c for c in data['commands'] if c['kind'] == 'package:test')['status'], 'hollow_candidate')

    def test_variable_reference_is_not_a_missing_literal_file(self):
        self.write('README.md', '`python3 "$PLUGIN_ROOT/scripts/audit-docs.py"`\n')
        data = self.run_health()
        self.assertEqual([g['reason'] for g in data['coverage_gaps']], ['dynamic_command_reference'])

    def test_compound_command_is_not_hollow(self):
        self.write('package.json', json.dumps({'scripts': {'test': 'echo starting && pytest tests'}}))
        self.assertEqual(self.run_health()['commands'][0]['status'], 'candidate_not_executed')

    def test_explicit_session_receipt_is_rejected(self):
        self.write('.codex/sessions/history.json', '{"status":"pass"}')
        data = self.run_health('--evidence', '.codex/sessions/history.json')
        self.assertEqual(data['receipts'], [])
        self.assertEqual(data['coverage_gaps'][0]['reason'], 'agent_private_directory_out_of_scope')

    def test_git_filter_is_not_executed(self):
        def git(*args):
            subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)
        git('init', '-q')
        self.write('test.txt', 'old\n')
        git('add', 'test.txt')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'base')
        self.write('.gitattributes', 'test.txt filter=probe\n')
        git('config', 'filter.probe.clean', 'touch EXECUTED; cat')
        self.write('test.txt', 'new\n')
        data = self.run_health()
        self.assertFalse((self.root / 'EXECUTED').exists())
        self.assertIsNone(data['git']['dirty'])

    def test_git_config_external_include_is_not_read(self):
        self.write('.git/HEAD', 'ref: refs/heads/main\n')
        self.write('.git/refs/heads/main', 'a' * 40 + '\n')
        outside = self.root.parent / 'outside.config'
        outside.write_text('this is deliberately invalid Git config')
        self.write('.git/config', '[include]\n    path = ' + str(outside) + '\n')
        data = self.run_health()
        self.assertEqual(data['git']['head'], 'a' * 40)

    def test_external_worktree_git_pointer_not_followed(self):
        self.write('.git', 'gitdir: /outside/worktree\n')
        self.assertEqual(self.run_health()['git']['status'], 'unavailable')

    def test_cli_secret_values_are_redacted(self):
        self.write('package.json', json.dumps({'scripts': {'test':
            'npm test --token SYNTHETIC_VALUE --password "quoted secret" api_key="assigned secret"'}}))
        data = self.run_health()
        output = json.dumps(data)
        for secret in ('SYNTHETIC_VALUE', 'quoted secret', 'assigned secret'):
            self.assertNotIn(secret, output)
        self.assertIn('[REDACTED]', output)

    def test_common_script_spellings_link_docs_and_ci(self):
        cases = [('./scripts/verify.sh', 'scripts/verify.sh'),
                 ('bash verify.sh', 'verify.sh'),
                 ('bash scripts/verify.sh', 'scripts/verify.sh'),
                 ('bash "scripts/check project.sh"', 'scripts/check project.sh'),
                 ('"./scripts/check project.sh"', 'scripts/check project.sh')]
        for command, name in cases:
            with self.subTest(command=command):
                self.write('README.md', '`' + command + '`\n')
                self.write('.github/workflows/test.yml', 'steps:\n  - run: ' + command + '\n')
                self.write(name, 'touch EXECUTED\npython3 -m unittest discover\n')
                data = self.run_health()
                commands = [c for c in data['commands'] if c['kind'] in ('instruction', 'ci')]
                self.assertEqual(len(commands), 2)
                for candidate in commands:
                    self.assertEqual(candidate['scripts'], [name])
                    self.assertTrue(candidate['same_literal_script_in_ci'])
                self.assertTrue(next(f['sha256'] for f in data['files'] if f['path'] == name))
                self.assertFalse((self.root / 'EXECUTED').exists())

    def test_assignments_do_not_hide_test_execution(self):
        cases = [('PYTHONPATH=.', 'hollow_candidate'),
                 ('A=one B="two words"', 'hollow_candidate'),
                 ('PYTHONPATH=. pytest tests', 'candidate_not_executed'),
                 ('A=one B="two words" pytest tests', 'candidate_not_executed'),
                 ('A="unterminated', 'candidate_not_executed')]
        for command, status in cases:
            with self.subTest(command=command):
                self.write('package.json', json.dumps({'scripts': {'test': command}}))
                self.write('README.md', '`bash scripts/verify.sh`\n')
                self.write('scripts/verify.sh', command + '\n')
                data = self.run_health()
                for kind in ('package:test', 'instruction'):
                    self.assertEqual(next(c['status'] for c in data['commands'] if c['kind'] == kind), status)

    def test_non_script_arguments_and_sha_fields_are_not_script_paths(self):
        self.write('README.md', '`python3 -m unittest discover -p test_project_health.py`\n')
        self.write('.github/workflows/test.yml',
                   'env:\n  BASE: ${{ github.event.pull_request.base.sha }}\n')
        data = self.run_health()
        self.assertEqual(data['coverage_gaps'], [])
        self.assertEqual(len(data['commands']), 1)
        self.assertEqual(data['commands'][0]['scripts'], [])

    def test_unparsed_ci_command_reports_gap(self):
        self.write('.github/workflows/test.yml', 'steps:\n  - run: custom-validator --all\n')
        data = self.run_health()
        self.assertIn('unrecognized_command', [g['reason'] for g in data['coverage_gaps']])

    def test_quoted_external_and_private_script_paths_stay_blocked(self):
        for command in ('bash "../outside script.sh"', 'bash "/tmp/outside script.sh"',
                        'bash ".codex/session script.sh"'):
            with self.subTest(command=command):
                self.write('README.md', '`' + command + '`\n')
                self.assertTrue(self.run_health()['coverage_gaps'])

    def test_bad_root_returns_execution_error(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root / 'missing')], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)['status'], 'error')


if __name__ == '__main__':
    unittest.main()
