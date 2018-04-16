#!/usr/bin/env bash

varLocalClearArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='file f "Storage file path" false'
  )
}

varLocalClear() {
  # If no file specified
  if [ -z "${FILE+x}" ]; then
    # Use wex tmp folder
    FILE=${WEX_DIR_TMP}variablesLocalStorage
  fi

  if [ ! -f ${FILE} ];then
    touch ${FILE}
  fi

  # Remove all previous values.
  wex config/removeKey -k="local\s"${NAME}"\=" -f=${FILE}
}
