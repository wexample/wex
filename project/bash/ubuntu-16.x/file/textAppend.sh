#!/usr/bin/env bash

fileTextAppendArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
    [1]='line l "New line" true'
    [2]='create c "Create if exists" false'
  )
}

fileTextAppend() {

  if [[ ${CREATE} == true ]];then
    wex file/createIfNotExists -f=${FILE}
  fi;

  # TODO Maybe this lines encoding may cause problem ?
  printf "\n${LINE}" >> ${FILE}
}
