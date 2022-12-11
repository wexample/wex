#!/usr/bin/env bash

varClearArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'file f "Storage file path" false'
  )
}

varClear() {
  # If no file specified
  if [ "${FILE}" == "" ];then
    # Use wex tmp folder
    FILE=${WEX_TMP_GLOBAL_VAR}
  fi

  if [ ! -f ${FILE} ];then
    touch ${FILE}
  fi

  # Remove all previous values.
  wex config/removeKey -k=${NAME}"\=" -f=${FILE}
}
