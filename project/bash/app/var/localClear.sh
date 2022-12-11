#!/usr/bin/env bash

varLocalClearArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'file f "Storage file path" false'
    'save_default s "Clear also last choice" false'
  )
}

varLocalClear() {
  # Remove all previous values.
  wex default::var/localClear -n="${NAME}" -f="${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}"

  if [ "${SAVE_DEFAULT}" = true ];then
    wex default::var/localClear -n="LAST_${NAME}"
  fi
}
