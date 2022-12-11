#!/usr/bin/env bash

varLocalClearArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='file f "Storage file path" false'
  )
}

varLocalClear() {
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
