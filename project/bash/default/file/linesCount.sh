#!/usr/bin/env bash

fileLinesCountArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
    [1]='ignore_empty i "Ignore empty lines" false'
  )
}

fileLinesCount() {
  if [ "${IGNORE_EMPTY}" == "true" ];then
    cat ${FILE} | sed '/^\[[:space:]]\{0,\}$/d' | wc -l
  else
    cat ${FILE} | wc -l | sed 's/^ *//'
  fi
}
