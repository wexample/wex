#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_ROOT="${APP_ROOT:-$ROOT}"
AM_DIR="$ROOT/.wex/python/app_manager"
WEX_TASK_ID="$(date '+%Y%m%d-%H%M%S-%N')-$$"

export APP_ROOT

if [[ "${1-}" == "checkup" ]]; then
  echo "Install"
  exit 0
fi

exec "$AM_DIR/.venv/bin/python" "$AM_DIR/__main__.py" "${WEX_TASK_ID}" "${@}"
