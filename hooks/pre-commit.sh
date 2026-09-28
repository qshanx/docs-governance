#!/usr/bin/env bash
# 可组合的提交护栏：暂存文档审计 + 原有日志约束。
set -uo pipefail
plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$plugin_root/scripts/check-staged-docs.py" --root "$PWD" || exit $?
bash "$plugin_root/templates/pre-commit.example"
