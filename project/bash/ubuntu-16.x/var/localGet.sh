#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
  )
}

varLocalGet() {
  local LOCAL_STORAGE_FILE=${WEX_DIR_TMP}variablesLocalStorage

  if [ -f ${LOCAL_STORAGE_FILE} ];then
    # Eval whole file.
    eval $(cat ${LOCAL_STORAGE_FILE})
    # Get value
    local VALUE=$(eval 'echo ${'${NAME}'}')

    if [ "${VALUE}" == "" ]; then
      echo ${DEFAULT}
    else
      echo ${VALUE}
    fi;
  fi
}
