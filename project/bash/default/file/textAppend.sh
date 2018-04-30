#!/usr/bin/env bash

fileTextAppendArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
    [1]='line l "New line" true'
    [2]='create c "Create if exists" false'
  )
}

fileTextAppend() {
  # To linux lines ending
  ORIGINAL=$(wex file/convertLinesToUnix -f=${FILE})

  if [ "${CREATE}" == true ];then
    wex file/createIfNotExists -f=${FILE}
  fi;

  printf "\n${LINE}" >> ${FILE}

  # Revert lines encoding format.
  wex file/convertLinesFormat -f=${FILE} -t=${ORIGINAL}
}
