from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit-docs.py"


class AuditDocsTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_audit(self, scope: str, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.project), "--scope", scope, *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_artifact_scope_fails_on_broken_markdown_link(self):
        (self.project / "guide.md").write_text("[缺失](docs/missing.md)\n", encoding="utf-8")
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Markdown 链接断裂", result.stdout)

    def test_json_reports_broken_link_with_machine_readable_evidence(self):
        (self.project / "guide.md").write_text("[缺失](docs/missing.md)\n", encoding="utf-8")
        text_result = self.run_audit("artifacts")
        result = self.run_audit("artifacts", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, text_result.returncode)
        self.assertEqual(report["exit_code"], 1)
        self.assertEqual(report["status"], "fail")
        finding = next(item for item in report["findings"] if item["check"] == "links.local")
        self.assertEqual(finding["status"], "fail")
        self.assertEqual(finding["scope"], "artifacts")
        self.assertEqual(finding["path"], "guide.md")
        self.assertEqual(finding["evidence"]["target"], "docs/missing.md")
        self.assertIn(finding["message"], text_result.stdout)

    def test_json_success_is_available_through_shell_adapter(self):
        (self.project / "guide.md").write_text("# 文档\n", encoding="utf-8")
        result = subprocess.run(
            ["bash", str(ROOT / "scripts/audit-cheap.sh"), "artifacts", "--format", "json"],
            cwd=self.project, env={**os.environ, "DOCS_GOVERNANCE_ROOT": str(self.project)},
            text=True, capture_output=True, check=False,
        )
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["scope"], "artifacts")
        self.assertEqual(Path(report["root"]), self.project.resolve())
        self.assertIsNone(report["head_commit"])
        self.assertIsNone(report["worktree_dirty"])

    def test_json_marks_absent_history_as_unverified_without_blocking_adoption(self):
        result = self.run_audit("spine", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["status"], "unverified")
        self.assertIsNone(report["base_ref"])
        finding = next(item for item in report["findings"] if item["check"] == "log.append-only")
        self.assertEqual(finding["status"], "unverified")

    def test_json_distinguishes_invalid_baseline_and_root_from_document_failures(self):
        for extra in (("--base-ref", "missing-ref"), ("--root", str(self.project / "absent"))):
            with self.subTest(extra=extra):
                result = self.run_audit("spine", "--format", "json", *extra)
                report = json.loads(result.stdout)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["exit_code"], 2)
                self.assertEqual(report["status"], "error")
                self.assertEqual(report["counts"]["fail"], 0)
                self.assertEqual(report["counts"]["error"], 1)

    def test_json_read_failure_does_not_become_a_pass(self):
        (self.project / "guide.md").write_bytes(b"\xff\xfe")
        result = self.run_audit("artifacts", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["findings"][-1]["check"], "audit.execution")

    def test_json_keeps_orphan_hint_separate_from_failure(self):
        (self.project / "docs").mkdir()
        (self.project / "docs/orphan.md").write_text("# 独立文档\n", encoding="utf-8")
        result = self.run_audit("artifacts", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["status"], "warning")
        finding = next(item for item in report["findings"] if item["check"] == "docs.orphans")
        self.assertEqual(finding["evidence"]["candidates"], ["docs/orphan.md"])

    def test_json_non_directory_link_parent_is_a_document_failure(self):
        (self.project / "note.txt").write_text("普通文件\n", encoding="utf-8")
        (self.project / "guide.md").write_text("[不存在](note.txt/missing.md)\n", encoding="utf-8")
        result = self.run_audit("artifacts", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "fail")
        finding = next(item for item in report["findings"] if item["check"] == "links.local")
        self.assertEqual(finding["evidence"]["target"], "note.txt/missing.md")

    def test_json_invalid_log_identifies_the_source_line(self):
        (self.project / "PROJECT_LOG.md").write_text(
            "# LOG\n\n[2026-09-05] fix | 格式错误\n", encoding="utf-8"
        )
        result = self.run_audit("spine", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        finding = next(item for item in report["findings"] if item["check"] == "log.format")
        self.assertEqual(finding["path"], "PROJECT_LOG.md")
        self.assertEqual(finding["line"], 3)

    def test_json_reports_corrupt_git_metadata_as_execution_error(self):
        subprocess.run(["git", "init"], cwd=self.project, capture_output=True, check=True)
        (self.project / ".git/config").write_text("invalid config line\n", encoding="utf-8")
        result = self.run_audit("artifacts", "--format", "json")
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["counts"]["error"], 1)
        shutil.rmtree(self.project / ".git")
        (self.project / ".git").write_text("gitdir: /missing/worktree-metadata\n", encoding="utf-8")
        result = self.run_audit("artifacts", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "error")

    def test_json_survives_symlink_cycles_in_root_and_link_targets(self):
        cycle = self.project / "cycle"
        cycle.symlink_to("cycle")
        (self.project / "guide.md").write_text("[循环](cycle)\n", encoding="utf-8")
        for extra in ((), ("--root", str(cycle))):
            with self.subTest(extra=extra):
                result = self.run_audit("artifacts", "--format", "json", *extra)
                report = json.loads(result.stdout)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["status"], "error")
                self.assertEqual(report["counts"]["error"], 1)

    def test_log_baseline_paths_are_relative_to_subproject_root(self):
        def git(*args):
            return subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", *args],
                cwd=self.project, text=True, capture_output=True, check=True,
            )
        subproject = self.project / "app"
        subproject.mkdir()
        log = subproject / "PROJECT_LOG.md"
        log.write_text("# LOG\n\n## [2026-09-05] init | 子项目首提\n", encoding="utf-8")
        git("init")
        git("add", "app/PROJECT_LOG.md")
        git("commit", "-m", "baseline")
        result = self.run_audit("spine", "--root", str(subproject), "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout)
        finding = next(item for item in json.loads(result.stdout)["findings"] if item["check"] == "log.append-only")
        self.assertEqual(finding["status"], "pass")
        log.write_text("# LOG\n", encoding="utf-8")
        result = self.run_audit("spine", "--root", str(subproject), "--format", "json")
        self.assertEqual(result.returncode, 1, result.stdout)
        finding = next(item for item in json.loads(result.stdout)["findings"] if item["check"] == "log.append-only")
        self.assertEqual(finding["status"], "fail")

    def test_json_records_git_baseline_and_uncommitted_changes(self):
        def git(*args):
            return subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", *args],
                cwd=self.project, text=True, capture_output=True, check=True,
            )
        git("init")
        log = self.project / "PROJECT_LOG.md"
        original = "# LOG\n\n## [2026-09-05] init | 首提\n"
        log.write_text(original, encoding="utf-8")
        git("add", "PROJECT_LOG.md")
        git("commit", "-m", "baseline")
        head = git("rev-parse", "HEAD").stdout.strip()
        for dirty in (False, True):
            if dirty:
                log.write_text(original + "## [2026-09-05] fix | 后续修改\n", encoding="utf-8")
            result = self.run_audit("spine", "--base-ref", "HEAD", "--format", "json")
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(report["head_commit"], head)
            self.assertEqual(report["base_ref"], head)
            self.assertEqual(report["requested_base_ref"], "HEAD")
            self.assertEqual(report["worktree_dirty"], dirty)

    def test_spine_scope_checks_architecture_paths(self):
        (self.project / "ARCHITECTURE.md").write_text(
            "# Architecture\n\nInterface 定义在 `src/missing.py`。\n",
            encoding="utf-8",
        )
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ARCHITECTURE.md -> src/missing.py", result.stdout)

    def test_spine_scope_does_not_treat_open_p0_paths_as_deleted(self):
        (self.project / "PROJECT_STATUS.md").write_text(
            "# Status\n\n## 红线\n\n### 删除区\n- 暂无\n\n### 未决 P0\n- `TESTS.md` 已建立。\n",
            encoding="utf-8",
        )
        (self.project / "TESTS.md").write_text("# TESTS\n", encoding="utf-8")
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("删除区无复活", result.stdout)

    def test_deleted_paths_are_checked_under_real_status_heading(self):
        status = (ROOT / "templates/PROJECT_STATUS.example.md").read_text(encoding="utf-8")
        (self.project / "PROJECT_STATUS.md").write_text(status, encoding="utf-8")
        old = self.project / "src/legacy_parser.py"
        old.parent.mkdir()
        old.touch()
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("删除区目标已复活：src/legacy_parser.py", result.stdout)

    def test_deleted_table_replacement_is_not_a_deleted_target(self):
        (self.project / "PROJECT_STATUS.md").write_text(
            "# Status\n\n### 删除区\n| 路径 | 替代物 |\n|---|---|\n"
            "| `legacy.py` | `current.py` |\n\n### 未决 P0\n- `current.py` 待检查\n",
            encoding="utf-8",
        )
        (self.project / "current.py").touch()
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_optional_bridge_references_allow_day_zero_but_required_paths_fail(self):
        (self.project / "AGENTS.md").write_text(
            (ROOT / "templates/AGENTS.example.md").read_text(encoding="utf-8"), encoding="utf-8"
        )
        (self.project / "CLAUDE.md").write_text("# 章程\n", encoding="utf-8")
        (self.project / "PROJECT_LOG.md").write_text("# LOG\n", encoding="utf-8")
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 0, result.stdout)
        (self.project / "CLAUDE.md").write_text("必读 `required.md`。\n", encoding="utf-8")
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("required.md", result.stdout)

    def test_reference_links_and_angle_destinations_are_checked(self):
        (self.project / "guide.md").write_text(
            '[安装][install]\n[install]: <docs/install guide.md> "安装"\n', encoding="utf-8"
        )
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 1, result.stdout)
        target = self.project / "docs/install guide.md"
        target.parent.mkdir()
        target.touch()
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_link_examples_in_code_are_not_live_links(self):
        (self.project / "guide.md").write_text(
            '```markdown\n[例子](missing.md)\n[ref]: other.md\n```\n'
            '`[内联例子](also-missing.md)`\n', encoding="utf-8"
        )
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_log_allows_only_git_renamed_link_targets(self):
        def git(*args):
            return subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", *args],
                cwd=self.project, text=True, capture_output=True, check=True,
            )
        git("init")
        old = self.project / "old.md"
        old.write_text("# Guide\n\nStable content.\n")
        log = self.project / "PROJECT_LOG.md"
        original = "## [2026-01-01] docs | read [guide](old.md#section)\n"
        log.write_text(original)
        git("add", ".")
        git("commit", "-m", "baseline")
        base = git("rev-parse", "HEAD").stdout.strip()
        old.rename(self.project / "new.md")
        migrated = original.replace("old.md", "new.md")
        log.write_text(migrated)
        git("add", ".")
        git("commit", "-m", "move")
        result = self.run_audit("spine", "--base-ref", base)
        self.assertEqual(result.returncode, 0, result.stdout)
        for changed in (migrated.replace("read", "rewrite"),
                        migrated.replace("[guide]", "[changed]"),
                        migrated.replace("#section", "#other"),
                        migrated.replace("new.md", "unrelated.md")):
            log.write_text(changed)
            result = self.run_audit("spine", "--base-ref", base)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("被删除或改写", result.stdout)

    def test_committed_log_rewrite_is_rejected_against_explicit_base(self):
        def git(*args):
            return subprocess.run(
                ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", *args],
                cwd=self.project, text=True, capture_output=True, check=True,
            )
        git("init")
        log = self.project / "PROJECT_LOG.md"
        log.write_text("# LOG\n\n## [2026-01-01] fix | original\n", encoding="utf-8")
        git("add", "PROJECT_LOG.md")
        git("commit", "-m", "baseline")
        base = git("rev-parse", "HEAD").stdout.strip()
        log.write_text("# LOG\n\n## [2026-01-01] fix | rewritten\n", encoding="utf-8")
        git("add", "PROJECT_LOG.md")
        git("commit", "-m", "rewrite")
        result = self.run_audit("spine", "--base-ref", base)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("被删除或改写", result.stdout)
        log.unlink()
        result = self.run_audit("spine", "--base-ref", base)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("被删除或改写", result.stdout)
        result = self.run_audit("spine", "--base-ref", "missing-ref")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("基准", result.stderr)

    def test_noncanonical_log_events_are_not_silently_ignored(self):
        (self.project / "PROJECT_LOG.md").write_text(
            "# LOG\n\n[2026-09-05] contract | 接口变更\n", encoding="utf-8"
        )
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("日志事件格式错误", result.stdout)

    def test_repository_audits_without_neighboring_checkouts(self):
        files = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
        ).decode().split("\0")
        for name in set(files):
            if not name or not (ROOT / name).is_file():
                continue
            target = self.project / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        result = self.run_audit("full")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_adr_scope_requires_every_file_in_index(self):
        adr_dir = self.project / "docs" / "adr"
        adr_dir.mkdir(parents=True)
        (adr_dir / "README.md").write_text("# ADR 索引\n", encoding="utf-8")
        (adr_dir / "0001-storage.md").write_text(
            "# ADR-0001\n\nStatus: accepted\n",
            encoding="utf-8",
        )
        result = self.run_audit("adr")
        self.assertEqual(result.returncode, 1)
        self.assertIn("未登记到统一索引", result.stdout)

    def test_adr_scope_accepts_indexed_decision(self):
        adr_dir = self.project / "docs" / "adr"
        adr_dir.mkdir(parents=True)
        (adr_dir / "README.md").write_text("[0001](0001-storage.md)\n", encoding="utf-8")
        (adr_dir / "0001-storage.md").write_text(
            "# ADR-0001\n\nStatus: accepted\n",
            encoding="utf-8",
        )
        result = self.run_audit("adr")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_adr_scope_rejects_missing_index_link(self):
        adr_dir = self.project / "docs" / "adr"
        adr_dir.mkdir(parents=True)
        (adr_dir / "README.md").write_text("[missing](0002-missing.md)\n", encoding="utf-8")
        result = self.run_audit("adr")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ADR 索引链接不存在", result.stdout)

    def test_adr_scope_rejects_missing_supersedes_target(self):
        adr_dir = self.project / "docs" / "adr"
        adr_dir.mkdir(parents=True)
        (adr_dir / "README.md").write_text("[new](0002-new.md)\n", encoding="utf-8")
        (adr_dir / "0002-new.md").write_text(
            "# ADR-0002\n\nStatus: accepted\n\n## Supersedes\n\n[old](0001-old.md)\n",
            encoding="utf-8",
        )
        result = self.run_audit("adr")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ADR Supersedes 目标不存在", result.stdout)

    def test_artifact_scope_rejects_unregistered_test_id_when_tests_ledger_exists(self):
        docs = self.project / "docs"
        docs.mkdir()
        (self.project / "TESTS.md").write_text("# TESTS\n\nTEST-ORDER-001\n", encoding="utf-8")
        (docs / "spec.md").write_text("需要 TEST-ORDER-002 验证。\n", encoding="utf-8")
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 1)
        self.assertIn("TEST-ID 未在 TESTS.md 登记", result.stdout)

    def test_artifact_scope_ignores_skill_names_plural_and_marked_examples(self):
        docs = self.project / "docs"
        docs.mkdir()
        (self.project / "TESTS.md").write_text("# TESTS\n\nTEST-AUDIT-001\n", encoding="utf-8")
        (docs / "guide.md").write_text(
            "test-collaboration 负责维护 TEST-IDs，真实证据见 TEST-AUDIT-001。\n",
            encoding="utf-8",
        )
        (self.project / "proposal.md").write_text(
            "<!-- test-id-audit: examples-only -->\n\n示例：TEST-ORDER-001。\n",
            encoding="utf-8",
        )
        result = self.run_audit("artifacts")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("跨文档 TEST-ID 均可回到 TESTS.md", result.stdout)

    def test_log_move_to_archive_preserves_append_only_history(self):
        subprocess.run(["git", "init"], cwd=self.project, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.project, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.project, check=True)
        old = "# LOG\n\n## [2026-01-01] init | one\n## [2026-01-02] fix | two\n"
        (self.project / "PROJECT_LOG.md").write_text(old, encoding="utf-8")
        subprocess.run(["git", "add", "PROJECT_LOG.md"], cwd=self.project, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.project, capture_output=True, check=True)

        (self.project / "PROJECT_LOG.md").write_text("# LOG\n\n## [2026-01-02] fix | two\n", encoding="utf-8")
        (self.project / "PROJECT_LOG.archive.md").write_text(
            "# archive\n\n## [2026-01-01] init | one\n",
            encoding="utf-8",
        )
        result = self.run_audit("spine")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("合并后保持只追加", result.stdout)


if __name__ == "__main__":
    unittest.main()
