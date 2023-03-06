#!/usr/bin/env bash

varClearArgs() {
  _DESCRIPTION="Remove a var from a config file"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'name n "Variable name" true'
    'file f "Storage file path" true '"${WEX_TMP_GLOBAL_VAR}"
  )
}

varClear() {
  if [ ! -f "${FILE}" ]; then
    touch "${FILE}"
  fi

  # Remove all previous values.
  wex-exec default::config/removeKey -k="${NAME}\=" -f="${FILE}"
}
