#!/usr/bin/env bash
# 可组合的提交护栏：检查暂存文档，不要求同批修改日志。
set -uo pipefail
plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$plugin_root/scripts/check-staged-docs.py" --root "$PWD" || exit $?
exit 0
