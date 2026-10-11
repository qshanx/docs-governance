"""Exercise the actual embedded path checker with isolated Skill references."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = (ROOT / "scripts/verify.sh").read_text().split("<<'PYREF'\n", 1)[1].split("\nPYREF", 1)[0]


class VerifyReferencesTest(unittest.TestCase):
    def check_reference(self, fragment, package_exists):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("README.md", "使用说明.md", "CLAUDE.md", "CLAUDE_MAP.md", "ARCHITECTURE.md"):
                (root / name).write_text("")
            skill = root / "skills/documentation/sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"[rules](references/writing-rules.md{fragment})")
            # A root-level decoy must not mask a missing package reference.
            (root / "references").mkdir()
            (root / "references/writing-rules.md").write_text("# Example\n")
            if package_exists:
                (skill / "references").mkdir()
                (skill / "references/writing-rules.md").write_text("# Example\n")
            return subprocess.run([sys.executable, "-c", CHECKER], cwd=root, capture_output=True, text=True)

    def test_package_links_with_and_without_fragments(self):
        for fragment in ("", "#example", "#章节"):
            with self.subTest(fragment=fragment):
                result = self.check_reference(fragment, True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_root_decoy_does_not_hide_missing_package_file(self):
        for fragment in ("", "#example"):
            with self.subTest(fragment=fragment):
                result = self.check_reference(fragment, False)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("sample/references/writing-rules.md", result.stdout)
