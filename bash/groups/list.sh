#!/usr/bin/env bash

groupsListArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='List all groups of a given path'
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'addon a "Addon name" false false'
    'filepath f "Return also script file path false false"'
  )
}

groupsList() {
  if [ "${ADDON}" = false ]; then
    local ADDON_BASH_DIR="${WEX_DIR_BASH}"
  else
    local ADDON_BASH_DIR="${WEX_DIR_ADDONS}${ADDON}/bash/${GROUP}/"
  fi

  if [ "${FILEPATH}" == "true" ]; then
    find "${ADDON_BASH_DIR}" -maxdepth 1 -type d -name "[a-zA-Z0-9]*" -exec realpath {} \;
  else
    for i in "${ADDON_BASH_DIR}"/*; do
      if [ -d "$i" ]; then
        echo "${i##*/}"
      fi
    done
  fi
}
