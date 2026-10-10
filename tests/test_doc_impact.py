import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/find-doc-impact.py'


class DocumentCandidatesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'

    def build(self, case='interface'):
        result = subprocess.run([sys.executable, str(ROOT / 'tests/fixtures/document-impact.py'),
                                 str(self.root), '--case', case], check=True, capture_output=True, text=True)
        self.fixture = json.loads(result.stdout)

    def scan(self, *extra):
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root),
                                 '--base', self.fixture['base'], *extra], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_interface_finds_unmapped_lines_and_keeps_counterexamples_as_candidates(self):
        self.build()
        result = self.scan('--head', self.fixture['head'])
        docs = {d['path']: d for d in result['candidates']}
        for name in ('api', 'consumer', 'integration'):
            doc = docs[f'docs/{name}.md']
            self.assertTrue(any(m['line'] == 3 and 'total' in m['text'] for m in doc['matches']))
            self.assertEqual(doc['status'], 'candidate')
        self.assertEqual(docs['docs/integration.md']['reasons'], [])  # 无映射仍可找到。
        self.assertTrue(any(r['kind'] == 'reference' for m in docs['docs/reference.md']['matches']
                            for r in m['reasons']))
        for name in ('history', 'inventory', 'reference'):
            self.assertEqual(docs[f'docs/{name}.md']['status'], 'candidate')
        self.assertEqual(result['skipped'], [])

    def test_committed_snapshot_ignores_local_fix_worktree_includes_it_and_untracked(self):
        self.build()
        path = self.root / 'docs/api.md'
        path.write_text(path.read_text().replace('"total"', '"total_amount"'))
        (self.root / 'docs/new.md').write_text('# New\nRead get_order()["total"].\n')
        committed = self.scan('--head', self.fixture['head'])
        docs = {d['path']: d for d in committed['candidates']}
        self.assertTrue(any('"total"' in m['text'] for m in docs['docs/api.md']['matches']))
        self.assertNotIn('docs/new.md', docs)
        live = self.scan('--worktree')
        docs = {d['path']: d for d in live['candidates']}
        self.assertTrue(any('"total_amount"' in m['text'] for m in docs['docs/api.md']['matches']))
        self.assertIn('docs/new.md', docs)
        self.assertIn('docs/new.md', live['worktree_sha256'])

    def test_function_change_can_use_domain_term_without_old_identifier_change(self):
        self.build('internal')
        # 字段和函数名不变，金额规则改变；业务术语需由 Agent 补充。
        source = self.root / 'src/api.py'
        source.write_text(source.read_text().replace('total=100', 'total=200'))
        (self.root / 'docs/feature.md').write_text('# 需求\n订单赠送金额固定为 100 分。\n')
        result = self.scan('--worktree', '--term', '订单赠送金额')
        doc = next(d for d in result['candidates'] if d['path'] == 'docs/feature.md')
        self.assertEqual(doc['matches'][0]['line'], 2)
        self.assertIn({'kind': 'term', 'term': '订单赠送金额', 'sources': ['explicit-term']},
                      doc['matches'][0]['reasons'])
        # 实现确实改变，但脚本不能自行决定修改已确认的需求。
        call = subprocess.run([sys.executable, '-B', '-c',
                               'from src.api import get_order; assert get_order()["total"] == 200'],
                              cwd=self.root, capture_output=True)
        self.assertEqual(call.returncode, 0)
        self.assertTrue(all(d['status'] == 'candidate' for d in result['candidates']))

    def test_deleted_path_symlink_and_invalid_baseline_are_not_silently_passed(self):
        self.build()
        (self.root / 'schema/order.json').unlink()
        (self.root / 'docs/external.md').symlink_to(self.root.parent / 'missing.md')
        result = self.scan('--worktree')
        self.assertIn('schema/order.json', result['changed_files'])
        self.assertTrue(any(d['path'] == 'docs/integration.md' for d in result['candidates']))
        self.assertTrue(any(s['path'] == 'docs/external.md' for s in result['skipped']))
        failed = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root),
                                 '--base', 'nonexistent-ref'], capture_output=True, text=True)
        self.assertEqual(failed.returncode, 2)
        self.assertEqual(failed.stdout, '')


if __name__ == '__main__':
    unittest.main()
