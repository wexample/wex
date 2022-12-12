#!/usr/bin/env bash

varClearArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'file f "Storage file path" true '"${WEX_TMP_GLOBAL_VAR}"
  )
}

varClear() {
  if [ ! -f "${FILE}" ];then
    touch "${FILE}"
  fi

  # Remove all previous values.
  wex config/removeKey -k="${NAME}\=" -f="${FILE}"
}
