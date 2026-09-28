from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-entrypoint-length.py"


class EntrypointLengthTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def run_check(self, *paths):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, paths)],
            capture_output=True, text=True, check=False,
        )

    def test_line_boundaries_and_line_endings(self):
        path = self.root / "AGENTS.md"
        content = ["# 规则", "", "<!-- 注释 -->", "```"] * 51
        for count in (199, 200, 201):
            for newline in ("\n", "\r\n"):
                for trailing in (False, True):
                    with self.subTest(count=count, newline=newline, trailing=trailing):
                        data = (newline.join(content[:count]) + (newline if trailing else "")).encode()
                        path.write_bytes(data)
                        result = self.run_check(path)
                        self.assertEqual(result.returncode, int(count > 200), result.stderr)
                        self.assertIn(f"({count}/200 行)", result.stdout)
                        self.assertEqual(path.read_bytes(), data)

    def test_multiple_files_keep_failure_and_check_nested_paths(self):
        nested = self.root / "模块 空格"
        nested.mkdir()
        long_path = nested / "CLAUDE.md"
        short_path = self.root / "AGENTS.md"
        long_path.write_text("规则\n" * 201, encoding="utf-8")
        short_path.write_text("规则\n", encoding="utf-8")
        for paths in ((long_path, short_path), (short_path, long_path)):
            result = self.run_check(*paths)
            self.assertEqual(result.returncode, 1, result.stderr)
            for path in paths:
                self.assertIn(str(path), result.stdout)

    def test_read_errors_are_not_reported_as_success(self):
        invalid = self.root / "CLAUDE.md"
        invalid.write_bytes(b"\xff")
        valid = self.root / "AGENTS.md"
        valid.write_text("规则\n" * 201, encoding="utf-8")
        for path in (self.root / "missing.md", self.root, invalid):
            result = self.run_check(path, valid)
            self.assertEqual(result.returncode, 2)
            self.assertIn(str(path), result.stderr)
            self.assertIn(str(valid), result.stdout)

    def test_no_files_is_an_error(self):
        self.assertEqual(self.run_check().returncode, 2)
