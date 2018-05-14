#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='value v "Variable value" true'
    [2]='file f "Storage file path" false'
  )
}

varLocalSet() {
  # Prevent sub with same variables.
  local LOCAL_FILE=${FILE}

  # If no file specified
  if [ "${LOCAL_FILE}" == "" ];then
    # Use wex tmp folder
    LOCAL_FILE=${WEX_DIR_TMP}globalVariablesLocalStorage
  fi

  if [ ! -f ${LOCAL_FILE} ];then
    touch ${LOCAL_FILE}
  fi

  wex var/localClear -n="${NAME}"

  # Remove all previous values.
  wex config/removeKey -k=${NAME}"\=" -f=${LOCAL_FILE}

  echo -e ${NAME}'='${VALUE} >> ${LOCAL_FILE}
}
