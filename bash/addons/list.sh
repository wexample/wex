#!/usr/bin/env bash

addonsListArgs() {
  _DESCRIPTION="List of actually installed addons."
  _ARGUMENTS=(
    'separator s "Separator" false " "'
  )
}

addonsList() {
  local FOLDERS=($(find "${WEX_DIR_ADDONS}" -maxdepth 1 -mindepth 1 -type d -not -path .))
  local FOLDER=""
  local ADDONS=""

  for FOLDER in "${FOLDERS[@]}"; do
    ADDONS="${ADDONS}$(basename "${FOLDER}")${SEPARATOR}"
  done

  ADDONS="${ADDONS%?}"

  wex array/sort -a="${ADDONS}" -s="${SEPARATOR}"
}
