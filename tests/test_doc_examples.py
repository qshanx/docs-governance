"""Execute examples read from the known, locally generated interface fixture only."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentExamplesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'

    def build(self, case):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'tests/fixtures/document-impact.py'),
             str(self.root), '--case', case], check=True, capture_output=True, text=True,
            timeout=30)
        self.fixture = json.loads(result.stdout)

    def examples(self):
        for name in ('api', 'consumer', 'integration'):
            path = f'docs/{name}.md'
            body = (self.root / path).read_text()
            matches = re.findall(r'`(get_order\(\)\["[a-z_]+"\])`', body)
            self.assertEqual(len(matches), 1, path)
            yield path + ':inline', [sys.executable, '-B', '-c',
                                    f'from src.api import get_order; print({matches[0]})']
        body = (self.root / 'docs/api.md').read_text()
        blocks = re.findall(r'```bash\n(.*?)\n```', body, re.S)
        self.assertEqual(len(blocks), 1)
        args = shlex.split(blocks[0])
        self.assertEqual(args[:2], ['python3', '-c'])
        self.assertEqual(len(args), 3)
        yield 'docs/api.md:bash', [sys.executable, '-B', *args[1:]]

    def run_example(self, args):
        return subprocess.run(args, cwd=self.root, capture_output=True, text=True, timeout=10)

    def assert_example_passes(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '100')

    def test_interface_examples_fail_then_pass_after_document_only_fix(self):
        self.build('interface')
        protected = ('src/api.py', 'schema/order.json', 'docs/history.md', 'docs/inventory.md')
        before = {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest() for p in protected}
        for location, args in self.examples():
            with self.subTest(before=location):
                result = self.run_example(args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("KeyError: 'total'", result.stderr)
        for name in ('api', 'consumer', 'integration'):
            path = self.root / f'docs/{name}.md'
            path.write_text(path.read_text().replace('["total"]', '["total_amount"]'))
        for location, args in self.examples():
            with self.subTest(after=location):
                self.assert_example_passes(self.run_example(args))
        self.assertEqual(before, {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest()
                                  for p in protected})

    def test_internal_change_keeps_document_examples_working(self):
        self.build('internal')
        for location, args in self.examples():
            with self.subTest(location=location):
                self.assert_example_passes(self.run_example(args))

    def test_successful_exit_with_wrong_document_output_is_rejected(self):
        self.build('internal')
        path = self.root / 'docs/api.md'
        path.write_text(path.read_text().replace('print(get_order()["total"])', 'print(99)'))
        location, args = list(self.examples())[-1]
        self.assertEqual(location, 'docs/api.md:bash')
        result = self.run_example(args)
        self.assertEqual(result.returncode, 0)
        with self.assertRaises(AssertionError):
            self.assert_example_passes(result)


if __name__ == '__main__':
    unittest.main()
