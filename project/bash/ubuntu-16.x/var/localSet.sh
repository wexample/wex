#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='value v "Variable value" true'
  )
}

varLocalSet() {
  local LOCAL_STORAGE_FILE=${WEX_DIR_TMP}variablesLocalStorage

  if [ ! -f ${LOCAL_STORAGE_FILE} ];then
    touch ${LOCAL_STORAGE_FILE}
  fi

  echo -e "\nlocal "${NAME}"="${VALUE} >> ${LOCAL_STORAGE_FILE}
}
