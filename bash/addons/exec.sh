#!/usr/bin/env bash

addonsExecArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Execute a bash command from every addon folder."
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'command c "Bash command to execute from every addon folder" false false'
  )
}

addonsExec() {
  local FOLDERS
  mapfile -d '' -t FOLDERS < <(find "${WEX_DIR_ADDONS}" -maxdepth 1 -mindepth 1 -type d -not -path '.*' -print0)
  local FOLDER=""

  for FOLDER in "${FOLDERS[@]}"; do
    cd "${FOLDER}"
    ${COMMAND}
  done
}
