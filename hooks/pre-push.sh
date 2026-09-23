#!/usr/bin/env bash
# 推送分支前审计将被发送的提交；保留 stdin 中的全部 ref 更新。
set -euo pipefail
plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$plugin_root/scripts/check-pr-docs.py" --pre-push --remote "${1:-origin}"
