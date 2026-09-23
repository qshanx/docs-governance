#!/usr/bin/env python3
"""文档治理确定性审计：先报告可机械证明的断链与完整性问题。"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

from docpolicy import check_policy
from logformat import LogFormatError, parse_entries


SPINE = ("CLAUDE.md", "CLAUDE_MAP.md", "PROJECT_STATUS.md", "PROJECT_LOG.md")
OPTIONAL_CARRIERS = ("AGENTS.md", "ARCHITECTURE.md", "CONTEXT.md", "CONTRACT.md", "TESTS.md", "REGRESSION.md")
LINK_DESTINATION = r'(<[^>\n]+>|(?:\\.|[^\s()]|\([^()]*\))+)'
MARKDOWN_LINK_RE = re.compile(r'\[[^\]\n]*\]\(\s*' + LINK_DESTINATION + r'(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE_LINK_RE = re.compile(r'^ {0,3}\[[^\]\n]+\]:\s*' + LINK_DESTINATION, re.MULTILINE)
CODE_PATH_RE = re.compile(r"`([^`\n]+)`")
OPTIONAL_PATH_RE = re.compile(r'<!--\s*governance:\s*optional=([^>]+?)\s*-->')
TEST_ID_RE = re.compile(r"\bTEST-(?:[A-Z0-9]+-)*\d+\b", re.IGNORECASE)
TEST_ID_EXAMPLE_MARKER = "<!-- test-id-audit: examples-only -->"
ADR_FILE_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
ADR_TARGET_RE = re.compile(r"\b\d{4}-[a-z0-9-]+\.md\b")
IGNORED_DIRS = {".git", ".governance", ".venv", "node_modules", "vendor", "__pycache__"}
IGNORED_REFERENCE_MARKERS = ("*", "{", "}", "<", ">", "…", "...")


@dataclass(frozen=True)
class Finding:
    check: str
    status: str
    scope: str
    message: str
    path: str | None
    line: int | None
    evidence: dict


class Report:
    def __init__(self, root: Path, scope: str, requested_base_ref: str | None) -> None:
        self.root = root
        self.scope = scope
        self.requested_base_ref = requested_base_ref
        self.base_ref: str | None = None
        self.head_commit: str | None = None
        self.worktree_dirty: bool | None = None
        self.findings: list[Finding] = []
        self.current_scope = scope

    def add(self, check: str, status: str, message: str, *, path: str | None = None,
            line: int | None = None, evidence: dict | None = None) -> None:
        self.findings.append(Finding(check, status, self.current_scope, message, path, line, evidence or {}))

    def result(self) -> dict:
        counts = {status: sum(item.status == status for item in self.findings)
                  for status in ("error", "fail", "unverified", "warning", "pass")}
        status = next((status for status, count in counts.items() if count), "unverified")
        return {
            "schema_version": 1,
            "root": str(self.root),
            "scope": self.scope,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "requested_base_ref": self.requested_base_ref,
            "base_ref": self.base_ref,
            "head_commit": self.head_commit,
            "worktree_dirty": self.worktree_dirty,
            "status": status,
            "exit_code": 2 if counts["error"] else 1 if counts["fail"] else 0,
            "counts": counts,
            "findings": [asdict(item) for item in self.findings],
        }

    def render(self, output_format: str) -> int:
        result = self.result()
        if output_format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            previous_scope = None
            symbols = {"pass": "✓", "warning": "⚠", "unverified": "?", "fail": "✗", "error": "!"}
            for item in self.findings:
                if item.scope != previous_scope:
                    print(f"\n[{item.scope}]")
                    previous_scope = item.scope
                stream = sys.stderr if item.status == "error" else sys.stdout
                print(f"  {symbols[item.status]} {item.message}", file=stream)
            print()
            if result["exit_code"] == 2:
                print("✗ 审计未完成：检查执行失败，不能据此判断文档是否通过。", file=sys.stderr)
            elif result["exit_code"] == 1:
                print(f"✗ 确定性审计失败：{result['counts']['fail']} 项。先修问题，再进入语义审计。")
            else:
                print("✓ 确定性审计未发现失败项；警告与未验证项需人工判断，可继续语义审计。")
        return result["exit_code"]


def markdown_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*.md"):
        if path.is_dir():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        result.append(path)
    return sorted(result)


def git_show(root: Path, relative: str, base_ref: str | None) -> str | None:
    if base_ref is None:
        return None
    entry = subprocess.run(
        ["git", "ls-tree", base_ref, "--", relative], cwd=root,
        text=True, capture_output=True, check=True,
    )
    if not entry.stdout.strip():
        return None
    command = subprocess.run(
        ["git", "show", f"{base_ref}:./{relative}"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    return command.stdout


def normalize_link_target(raw: str) -> str | None:
    target = raw.strip().strip("<>")
    target = unquote(target.split("#", 1)[0])
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
        return None
    return target


def markdown_targets(text: str) -> list[str]:
    """检查内联链接和引用定义；代码示例不是活动链接。"""
    prose: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and marker:
            fence = marker.group(1)
            continue
        if fence is not None:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
            continue
        if line.startswith(("    ", "\t")):
            continue
        prose.append(re.sub(r"(`+).*?\1", "", line))
    content = "\n".join(prose)
    return MARKDOWN_LINK_RE.findall(content) + REFERENCE_LINK_RE.findall(content)


def resolve_path(path: Path) -> Path:
    # strict 模式在各 Python 版本都报告循环链接；普通缺失路径留给文档检查判定。
    try:
        return path.resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError):
        return path.resolve()


def resolve_target(root: Path, source: Path, target: str) -> Path:
    if target.startswith("/"):
        return resolve_path(Path(target))
    return resolve_path(source.parent / target)


def check_markdown_links(root: Path, files: list[Path], report: Report) -> None:
    broken: list[tuple[str, str]] = []
    for source in files:
        if "templates" in source.relative_to(root).parts:
            continue
        text = source.read_text(encoding="utf-8")
        for raw in markdown_targets(text):
            target = normalize_link_target(raw)
            if target is None:
                continue
            resolved = resolve_target(root, source, target)
            if not resolved.exists():
                broken.append((source.relative_to(root).as_posix(), target))
    if broken:
        for source, target in sorted(set(broken)):
            report.add("links.local", "fail", f"Markdown 链接断裂：{source} -> {target}",
                       path=source, evidence={"target": target})
    else:
        report.add("links.local", "pass", "Markdown 本地链接无断链")


def plausible_code_path(value: str) -> bool:
    if any(marker in value for marker in IGNORED_REFERENCE_MARKERS):
        return False
    if any(character.isspace() for character in value):
        return False
    if value.startswith(("http://", "https://", "$", ".governance/")):
        return False
    if re.fullmatch(r"/[a-z0-9-]+", value):
        return False
    return "/" in value or value.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml"))


def check_spine_paths(root: Path, report: Report) -> None:
    broken: list[tuple[str, str]] = []
    for name in ("CLAUDE.md", "CLAUDE_MAP.md") + OPTIONAL_CARRIERS:
        source = root / name
        if not source.exists():
            continue
        for line in source.read_text(encoding="utf-8").splitlines():
            optional = {
                value.strip()
                for declaration in OPTIONAL_PATH_RE.findall(line)
                for value in declaration.split(",")
            }
            for value in CODE_PATH_RE.findall(line):
                if not plausible_code_path(value):
                    continue
                candidate = Path(value)
                resolved = candidate if candidate.is_absolute() else root / candidate
                if not resolved.exists() and value not in optional:
                    broken.append((name, value))
    if broken:
        for name, target in sorted(set(broken)):
            report.add("spine.paths", "fail", f"脊柱/载体路径不存在：{name} -> {target}",
                       path=name, evidence={"target": target})
    else:
        report.add("spine.paths", "pass", "脊柱与可选载体中的路径引用存在")


def check_status_resurrection(root: Path, report: Report) -> None:
    status = root / "PROJECT_STATUS.md"
    if not status.exists():
        report.add("status.deleted", "unverified", "缺少 PROJECT_STATUS.md，跳过删除区检查", path="PROJECT_STATUS.md")
        return
    text = status.read_text(encoding="utf-8")
    resurrected: list[str] = []
    depth: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)", line)
        if heading:
            if heading.group(2).startswith("删除区"):
                depth = len(heading.group(1))
            elif depth is not None and len(heading.group(1)) <= depth:
                depth = None
            continue
        if depth is None:
            continue
        # 模板的第一列是删除路径，后续列可能引用仍应存在的替代物。
        value_column = line.strip().split("|")[1] if line.lstrip().startswith("|") else line
        for value in CODE_PATH_RE.findall(value_column)[:1]:
            if plausible_code_path(value) and (root / value).exists():
                resurrected.append(value)
    if resurrected:
        for value in sorted(set(resurrected)):
            report.add("status.deleted", "fail", f"删除区目标已复活：{value}",
                       path="PROJECT_STATUS.md", evidence={"target": value})
    else:
        report.add("status.deleted", "pass", "删除区无复活", path="PROJECT_STATUS.md")


def check_log(root: Path, report: Report, threshold: int, base_ref: str | None) -> None:
    active_path = root / "PROJECT_LOG.md"
    archive_path = root / "PROJECT_LOG.archive.md"
    if not active_path.exists():
        report.add("log.source", "unverified", "缺少 PROJECT_LOG.md，仍核对基准历史与现存归档", path="PROJECT_LOG.md")

    active_text = active_path.read_text(encoding="utf-8") if active_path.exists() else ""
    archive_text = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    _, active_entries = parse_entries(active_text, active_path.name)
    _, archive_entries = parse_entries(archive_text, archive_path.name)
    current_events = {entry.content for entry in active_entries + archive_entries}
    previous_events: set[str] = set()
    for relative in ("PROJECT_LOG.md", "PROJECT_LOG.archive.md"):
        previous = git_show(root, relative, base_ref)
        if previous is not None:
            _, entries = parse_entries(previous, relative)
            previous_events.update(entry.content for entry in entries)
    missing = previous_events - current_events
    if missing:
        report.add("log.append-only", "fail", f"PROJECT_LOG 历史有 {len(missing)} 条被删除或改写，且未原样进入归档",
                   path="PROJECT_LOG.md", evidence={"missing_count": len(missing)})
    elif base_ref is not None:
        report.add("log.append-only", "pass", "PROJECT_LOG 活跃文件与归档合并后保持只追加", path="PROJECT_LOG.md")
    else:
        report.add("log.append-only", "unverified", "无 Git 提交基准，历史只追加完整性未验证", path="PROJECT_LOG.md")

    count = len(active_entries)
    message = (f"PROJECT_LOG 活跃事件 {count} 条，超过 {threshold}；应先复盘，再归档并重建 SQLite 索引"
               if count > threshold else f"PROJECT_LOG 活跃事件 {count} 条，未超过 {threshold}")
    report.add("log.event-count", "warning" if count > threshold else "pass", message,
               path="PROJECT_LOG.md", evidence={"count": count, "threshold": threshold})

    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", ".governance/project-log.sqlite"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if tracked.returncode == 0:
        report.add("log.index-untracked", "fail", ".governance/project-log.sqlite 是派生索引，不应提交进 git",
                   path=".governance/project-log.sqlite")


def parse_adr_status(text: str) -> str | None:
    patterns = (
        r"(?im)^[-*]?\s*(?:status|状态)\s*[:：]\s*`?([a-z]+)`?\s*$",
        r"(?im)^##\s+(?:status|状态)\s*\n+\s*`?([a-z]+)`?\s*$",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).lower()
    return None


def check_adr(root: Path, report: Report) -> None:
    adr_dir = root / "docs" / "adr"
    if not adr_dir.exists():
        report.add("adr.index", "unverified", "docs/adr/ 尚未创建；ADR 按实际决策懒创建", path="docs/adr")
        return
    index = adr_dir / "README.md"
    if not index.exists():
        report.add("adr.index", "fail", "docs/adr/ 存在但缺少 README.md 统一索引", path="docs/adr/README.md")
        return
    index_text = index.read_text(encoding="utf-8")
    for raw in markdown_targets(index_text):
        target = normalize_link_target(raw)
        if target is not None and target.endswith(".md") and not resolve_target(root, index, target).exists():
            report.add("adr.index", "fail", f"ADR 索引链接不存在：docs/adr/README.md -> {target}",
                       path="docs/adr/README.md", evidence={"target": target})
    adr_files = sorted(path for path in adr_dir.glob("*.md") if ADR_FILE_RE.match(path.name))
    missing_from_index = [path.name for path in adr_files if path.name not in index_text]
    for name in missing_from_index:
        report.add("adr.index", "fail", f"ADR 未登记到统一索引：docs/adr/{name}", path=f"docs/adr/{name}")

    allowed = {"proposed", "accepted", "deprecated", "superseded"}
    for path in adr_files:
        text = path.read_text(encoding="utf-8")
        status = parse_adr_status(text)
        if status is None:
            report.add("adr.status", "fail", f"ADR 缺少可解析状态：{path.relative_to(root)}", path=path.relative_to(root).as_posix())
        elif status not in allowed:
            report.add("adr.status", "fail", f"ADR 状态不受支持：{path.relative_to(root)} -> {status}",
                       path=path.relative_to(root).as_posix(), evidence={"status": status})
        supersedes = re.search(r"(?ims)^##\s+Supersedes\s*\n(?P<body>.*?)(?:\n## |\Z)", text)
        if supersedes and supersedes.group("body").strip().lower() not in {"none", "无"}:
            targets = ADR_TARGET_RE.findall(supersedes.group("body"))
            if not targets:
                report.add("adr.supersedes", "unverified", f"ADR Supersedes 无法机械解析，需人工核对：{path.relative_to(root)}",
                           path=path.relative_to(root).as_posix())
            for target in targets:
                if not (adr_dir / target).exists():
                    report.add("adr.supersedes", "fail", f"ADR Supersedes 目标不存在：{path.relative_to(root)} -> {target}",
                               path=path.relative_to(root).as_posix(), evidence={"target": target})
    if not missing_from_index and all(parse_adr_status(path.read_text(encoding="utf-8")) in allowed for path in adr_files):
        report.add("adr.status", "pass", f"ADR 索引登记与 {len(adr_files)} 个决策文件状态检查通过",
                   path="docs/adr/README.md", evidence={"count": len(adr_files)})


def check_test_ids(root: Path, files: list[Path], report: Report) -> None:
    tests_file = root / "TESTS.md"
    refs: set[str] = set()
    for path in files:
        parts = path.relative_to(root).parts
        if path == tests_file or any(
            section in parts for section in ("templates", "skills", "commands", "agents", "references")
        ):
            continue
        text = path.read_text(encoding="utf-8")
        if TEST_ID_EXAMPLE_MARKER in text:
            continue
        refs.update(value.upper() for value in TEST_ID_RE.findall(text))
    if not refs:
        report.add("tests.references", "pass", "未发现跨文档 TEST-ID 引用")
        return
    if not tests_file.exists():
        report.add("tests.references", "unverified", f"发现 {len(refs)} 个具体 TEST-ID 引用，但项目未启用 TESTS.md；需人工判断是否只是方案示例",
                   path="TESTS.md", evidence={"references": sorted(refs)})
        return
    defined = {value.upper() for value in TEST_ID_RE.findall(tests_file.read_text(encoding="utf-8"))}
    missing = refs - defined
    if missing:
        report.add("tests.references", "fail", "TEST-ID 未在 TESTS.md 登记：" + ", ".join(sorted(missing)),
                   path="TESTS.md", evidence={"missing": sorted(missing)})
    else:
        report.add("tests.references", "pass", "跨文档 TEST-ID 均可回到 TESTS.md", path="TESTS.md")


def check_orphans(root: Path, files: list[Path], report: Report) -> None:
    candidates = [
        path
        for path in files
        if "docs" in path.relative_to(root).parts
        and "templates" not in path.relative_to(root).parts
        and path.name != "README.md"
    ]
    all_text = {path: path.read_text(encoding="utf-8") for path in files}
    orphans: list[str] = []
    for candidate in candidates:
        relative = candidate.relative_to(root).as_posix()
        if not any(
            path != candidate and (relative in text or candidate.name in text)
            for path, text in all_text.items()
        ):
            orphans.append(relative)
    if orphans:
        report.add("docs.orphans", "warning", "疑似孤儿文档（需人工判断挂索引或归档）：" + ", ".join(orphans),
                   evidence={"candidates": orphans})
    else:
        report.add("docs.orphans", "pass", "docs/ 下未发现疑似孤儿文档")


def check_spine(root: Path, report: Report, threshold: int, base_ref: str | None) -> None:
    report.current_scope = "spine"
    for name in SPINE:
        if (root / name).exists():
            report.add("spine.carrier", "pass", f"{name} 存在", path=name)
        else:
            report.add("spine.carrier", "unverified", f"{name} 缺失（渐进采用时可能合理）", path=name)
    check_spine_paths(root, report)
    check_status_resurrection(root, report)
    check_log(root, report, threshold, base_ref)


def check_context(root: Path, report: Report) -> None:
    report.current_scope = "context"
    context = root / "CONTEXT.md"
    if not context.exists():
        report.add("context.carrier", "unverified", "CONTEXT.md 未创建；没有稳定领域词汇时无需补空壳", path="CONTEXT.md")
        return
    report.add("context.carrier", "pass", "CONTEXT.md 存在；术语边界与代码一致性留给语义层判断", path="CONTEXT.md")


def check_artifacts(root: Path, report: Report) -> None:
    report.current_scope = "artifacts"
    files = markdown_files(root)
    check_markdown_links(root, files, report)
    check_test_ids(root, files, report)
    check_orphans(root, files, report)
    check_policy(root, report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--scope", choices=("spine", "context", "adr", "artifacts", "full"), default="full")
    parser.add_argument("--log-threshold", type=int, default=200)
    parser.add_argument("--base-ref", help="日志历史比较基准；PR 传入基线提交，本地默认 HEAD")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="输出格式；JSON 包含范围、版本信息和结构化发现")
    args = parser.parse_args()

    root = args.root.absolute()
    report = Report(root, args.scope, args.base_ref)
    try:
        root = resolve_path(root)
        report.root = root
        if not root.is_dir():
            report.add("audit.root", "error", f"不是目录：{root}", path=str(root))
            return report.render(args.format)
        repository = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], cwd=root,
            text=True, capture_output=True, check=False, env={**os.environ, "LC_ALL": "C"},
        )
        if repository.returncode and not repository.stderr.startswith("fatal: not a git repository (or any"):
            repository.check_returncode()
        if repository.returncode == 0 and repository.stdout.strip() == "true":
            head = subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD^{commit}"], cwd=root,
                text=True, capture_output=True, check=False,
            )
            report.head_commit = head.stdout.strip() if head.returncode == 0 else None
            status = subprocess.run(
                ["git", "--no-optional-locks", "status", "--porcelain", "--untracked-files=normal"],
                cwd=root, text=True, capture_output=True, check=True,
            )
            report.worktree_dirty = bool(status.stdout.strip())
        if args.scope in ("spine", "full"):
            report.current_scope = "spine"
            if args.base_ref is not None:
                baseline = subprocess.run(
                    ["git", "rev-parse", "--verify", "--end-of-options", f"{args.base_ref}^{{commit}}"],
                    cwd=root, text=True, capture_output=True, check=False,
                )
                if baseline.returncode:
                    report.add("log.baseline", "error", f"无法解析日志比较基准：{args.base_ref}",
                               evidence={"requested_ref": args.base_ref})
                    return report.render(args.format)
                report.base_ref = baseline.stdout.strip()
            else:
                report.base_ref = report.head_commit
            try:
                check_spine(root, report, args.log_threshold, report.base_ref)
            except LogFormatError as exc:
                report.add("log.format", "fail", str(exc), path=exc.source_file, line=exc.source_line)
        if args.scope in ("context", "full"):
            check_context(root, report)
        if args.scope in ("adr", "full"):
            report.current_scope = "adr"
            check_adr(root, report)
        if args.scope in ("artifacts", "full"):
            check_artifacts(root, report)
    except (OSError, UnicodeError, RuntimeError, subprocess.SubprocessError) as exc:
        filename = getattr(exc, "filename", None)
        path = Path(filename) if filename else None
        location = path.relative_to(root).as_posix() if path and path.is_relative_to(root) else str(path) if path else None
        report.add("audit.execution", "error", f"检查执行失败：{exc}", path=location,
                   evidence={"exception": type(exc).__name__})
    return report.render(args.format)


if __name__ == "__main__":
    raise SystemExit(main())
