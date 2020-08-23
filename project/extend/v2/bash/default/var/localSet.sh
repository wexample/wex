#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='value v "Variable value" true'
    [2]='file f "Storage file path" false'
  )
}

varLocalSet() {
  # If no file specified
  if [ "${FILE}" = "" ];then
    # Use wex tmp folder
    FILE=${WEX_DIR_TMP}globalVariablesLocalStorage
  fi

  if [ ! -f ${FILE} ];then
    touch ${FILE}
  fi

  wex var/localClear -n="${NAME}"

  # Remove all previous values.
  wex config/removeKey -k=${NAME}"\=" -f=${FILE}

  echo -e "${NAME}=${VALUE}" >> ${FILE}
}
