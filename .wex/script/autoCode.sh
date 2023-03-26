#!/usr/bin/env bash

_wexMessage "Use this file to paste custom code, then rollback it before commit."

CURRENT_WEX_ROOT="$(realpath "$(dirname "$(realpath ${BASH_SOURCE[0]})")/../../")/"

# Code is executed from project's root directory.

_wexLog "Updating addons..."
for ADDON in "${WEX_ADDONS[@]}"; do
  ADDON_PATH=$(echo ${CURRENT_WEX_ROOT}addons/${ADDON})
  if [ -d "${ADDON_PATH}" ]; then
    _wexLog "Updating ${ADDON}..."

    cd ${CURRENT_WEX_ROOT}addons/${ADDON}

    # git commit ...
  fi
done
