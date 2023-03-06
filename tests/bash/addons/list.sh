#!/usr/bin/env bash

addonsListTest() {
  local ADDONS=($(wex-exec addons/list))
  local IS_ARRAY=false
  if [[ "$(declare -p ADDONS)" =~ "declare -a" && -n "${ADDONS[0]}" ]]; then
    IS_ARRAY=true
  fi

  _wexTestAssertEqual "${IS_ARRAY}" "true"
}
