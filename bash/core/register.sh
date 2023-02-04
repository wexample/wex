#!/usr/bin/env bash

coreRegisterArgs() {
  _DESCRIPTION="Create a local core registries."
}

coreRegister() {
  local LOCATIONS=$(_wexFindScriptsLocations)
  local ALL_SCRIPTS=()

  for LOCATION in ${LOCATIONS[@]}; do
    ALL_SCRIPTS+=($(wex scripts/list -d="${LOCATION}"))
  done

  echo "${ALL_SCRIPTS[@]}" | tr ' ' '\n' | sort > "${WEX_DIR_TMP}all-scripts"
}
