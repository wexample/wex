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
  if [ -z "${FILE+x}" ]; then
    # Use wex tmp folder
    FILE=${WEX_DIR_TMP}variablesLocalStorage
  fi

  if [ ! -f ${FILE} ];then
    touch ${FILE}
  fi

  echo -e 'local '${NAME}'='${VALUE} >> ${FILE}
}
