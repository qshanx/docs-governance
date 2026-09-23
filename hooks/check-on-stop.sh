#!/usr/bin/env bash
# docs-governance · Claude Code / Codex Stop hook
# 会话结束时检查四件套是否在腐烂，只提醒不阻塞（exit 0）。
# 强制检查在暂存审计和 CI；Stop 保持非阻塞，避免反复触发。
set -uo pipefail

plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 与直接调用 auto-audit 共用根定位；无法定位时报告原因但不阻塞会话。
governance_root="$(python3 "$plugin_root/scripts/auto-audit.py" --resolve-root)" || exit 0
cd -- "$governance_root" || { echo 'docs-governance: 无法进入治理根，本次未执行审计' >&2; exit 0; }

# 项目显式采用规则后，按内容变化调用同一审计器；Stop 只报告。
if [ -e .docs-governance.json ] || [ -L .docs-governance.json ]; then
  python3 "$plugin_root/scripts/auto-audit.py" --root "$PWD"
  exit 0
fi

quad=(CLAUDE.md CLAUDE_MAP.md PROJECT_STATUS.md PROJECT_LOG.md)
present=()
for f in "${quad[@]}"; do [ -f "$f" ] && present+=("$f"); done
# 没用四件套的项目，直接放行
[ ${#present[@]} -eq 0 ] && exit 0

warned=0

today=$(date +%Y-%m-%d)

# 检查1：相对时间残留（只查记录事实的 LOG/STATUS；CLAUDE.md / MAP 是结构文档，
# 章节标题叫"最近审计"、导航行写"最近发生什么→看 LOG"都是正当的，不算腐烂）
targets=()
for f in PROJECT_LOG.md PROJECT_STATUS.md; do [ -f "$f" ] && targets+=("$f"); done
if [ ${#targets[@]} -gt 0 ]; then
  # 只查"记录事实"的正文行，排除四类结构性文本（它们里出现相对时间是正当的）：
  #   1. 标题行 —— 章节叫"最近审计"合理，不该改成"2026-07-13 审计"
  #   2. 代码块 —— 路径占位符如 <今天> 是示例，不是事实
  #   3. 表格行 —— 图例/指标/维护规则表，如"| 最近审计 | 每次跑完追加一行 |"是在讲怎么维护
  #   4. 导航行 —— 如"想知道最近发生什么 → 看 PROJECT_LOG.md"是指路，不是记事
  rot=$(awk '
    /^```/ { in_code = !in_code; next }
    in_code { next }
    /^[[:space:]]*#/ { next }
    /^[[:space:]]*\|/ { next }
    /PROJECT_LOG\.md|PROJECT_STATUS\.md|CLAUDE_MAP\.md/ { next }
    /今天|昨天|刚刚|最近|上周|本周|recently|yesterday/ { print FILENAME ":" FNR ":" $0 }
  ' "${targets[@]}" 2>/dev/null || true)
  if [ -n "$rot" ]; then
    echo "⚠️ docs-governance: LOG/STATUS 里有相对时间，应改绝对日期（如 ${today}）：" >&2
    echo "$rot" >&2
    warned=1
  fi
fi

# 检查2：PROJECT_LOG 今天有没有追加（本会话有进展就该补一行）
if [ -f PROJECT_LOG.md ]; then
  if ! grep -q "${today}" PROJECT_LOG.md 2>/dev/null; then
    echo "⚠️ docs-governance: PROJECT_LOG.md 今天（${today}）还没有条目，这次会话有进展记得追加一行 ## [日期] 类型 | 摘要。" >&2
    warned=1
  fi
fi

[ "$warned" -eq 1 ] && echo "（以上为 docs-governance 治理提醒，不阻塞；要强制可把 hook 脚本结尾改 exit 2）" >&2
exit 0
