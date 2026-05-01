#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="/etc/wex.conf"
if [[ -f "$CONFIG_FILE" ]]; then source "$CONFIG_FILE"; fi

if [[ -z "${CORE_BIN:-}" ]]; then
    CORE_BIN="$(which wex 2>/dev/null || true)"
fi

if [[ -z "${CORE_BIN:-}" ]]; then
    echo "Error: Unable to locate 'wex'."
    exit 1
fi

exec "$CORE_BIN" "$@"
