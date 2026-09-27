#!/usr/bin/env bash
# 插件结构完整性自检：manifest / hook / 路由 / 引用 / Python 脚本与单元测试。
# 这是插件自己的"测试"——任何一处断链 exit 1，可挂进 CI 或发布前手动跑。
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
FAIL=0
ok(){ echo "  ✓ $1"; }
bad(){ echo "  ✗ $1"; FAIL=1; }

echo "[1] JSON 可解析"
for j in .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json hooks/hooks.json; do
  [ -f "$j" ] || { echo "  – $j 不存在，跳过"; continue; }
  python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$j" 2>/dev/null && ok "$j" || bad "$j 解析失败"
done

echo "[2] Claude / Codex manifest 一致"
python3 -c '
import json
from pathlib import Path
claude = json.loads(Path(".claude-plugin/plugin.json").read_text())
codex = json.loads(Path(".codex-plugin/plugin.json").read_text())
assert claude["name"] == codex["name"], "name 不一致"
assert claude["version"] == codex["version"], "version 不一致"
assert codex.get("skills") == "./skills/", "Codex skills 路径必须是 ./skills/"
' 2>/dev/null && ok "双端 name / version / skills 一致" || bad "Claude / Codex manifest 不一致"

echo "[3] hook 脚本可执行"
shopt -s nullglob
for h in hooks/*.sh; do [ -x "$h" ] && ok "$h" || bad "$h 不可执行（chmod +x）"; done

echo "[4] 每个 agent / skill 都有人引用或登记"
for a in agents/*.md; do
  name=$(basename "$a" .md)
  grep -rql "$name" commands/ skills/ README.md 2>/dev/null && ok "agents/$name 被引用" || bad "agents/$name 是孤儿（无 command/skill/README 引用）"
done
for d in skills/*/; do
  name=$(basename "$d")
  grep -q "$name" README.md 2>/dev/null || bad "skills/$name 未在 README 登记"
  grep -q "$name" 使用说明.md 2>/dev/null || bad "skills/$name 未在使用说明登记"
  if [ "$name" != "docs-governance" ]; then
    grep -q "$name" skills/docs-governance/SKILL.md 2>/dev/null || bad "skills/$name 未进入总路由"
  fi
  ok "skills/$name 文档与路由检查完成"
done

echo "[5] 路径式引用存在"
REF_PATTERN='(templates|references)/[A-Za-z0-9._-]+\.md|skills/[A-Za-z0-9._-]+/SKILL\.md|scripts/[A-Za-z0-9._-]+\.(py|sh)|docs/adr/[A-Za-z0-9._-]+\.md'
grep -rhoE "$REF_PATTERN" agents/ skills/ commands/ README.md 使用说明.md CLAUDE.md CLAUDE_MAP.md ARCHITECTURE.md docs/adr 2>/dev/null | sort -u | while read -r ref; do
  [ -f "$ref" ] && ok "$ref" || bad "$ref 被引用但不存在"
done
# 子 shell 里的 FAIL 不外传，单独复核第 5 项
MISS=$(grep -rhoE "$REF_PATTERN" agents/ skills/ commands/ README.md 使用说明.md CLAUDE.md CLAUDE_MAP.md ARCHITECTURE.md docs/adr 2>/dev/null | sort -u | while read -r ref; do [ -f "$ref" ] || echo "$ref"; done)
[ -n "$MISS" ] && FAIL=1

echo "[6] 每个 skill 有 SKILL.md / 每个 command 与 agent 是 .md"
for d in skills/*/; do [ -f "$d/SKILL.md" ] && ok "$d" || bad "$d 缺 SKILL.md"; done
for command in commands/*.md; do
  [ -f "$command" ] || continue
  if grep -qE 'skills/[A-Za-z0-9._-]+/SKILL\.md' "$command"; then
    ok "$command 委托共享 Skill"
  else
    bad "$command 未委托共享 Skill"
  fi
done

echo "[7] 日志派生索引不会进入 git"
git check-ignore -q .governance/project-log.sqlite 2>/dev/null && ok ".governance/ 已忽略" || bad ".governance/ 未进入 .gitignore"

echo "[8] Python 脚本可编译"
python3 -c 'from pathlib import Path
for pattern in ("scripts/*.py", "tests/*.py"):
    for path in Path(".").glob(pattern):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
' 2>/dev/null && ok "Python compile" || bad "Python 脚本编译失败"

echo "[9] 单元测试"
if ! python3 -c 'import jsonschema, openapi_spec_validator' 2>/dev/null; then
  bad "缺少开发测试依赖：激活虚拟环境后运行 python -m pip install -r requirements-dev.txt"
fi
python3 -m unittest discover -s tests -p 'test_*.py' >/tmp/docs-governance-unittest.log 2>&1
TEST_EXIT=$?
if [ "$TEST_EXIT" -eq 0 ]; then
  ok "unit tests"
else
  bad "unit tests 失败"
  sed 's/^/      /' /tmp/docs-governance-unittest.log
fi

echo "[10] 当前文档与日志历史审计"
bash scripts/audit-cheap.sh full && ok "full 文档审计" || bad "full 文档审计失败"

echo ""
if [ "$FAIL" -eq 0 ]; then echo "✅ verify 通过：插件结构完整，无断链。"; else echo "❌ verify 失败：见上面 ✗。"; fi
exit "$FAIL"
