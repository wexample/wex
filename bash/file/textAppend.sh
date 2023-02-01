#!/usr/bin/env bash

fileTextAppendArgs() {
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
    'create c "Create if exists" false'
  )
}

fileTextAppend() {
  if [ "${CREATE}" = "true" ];then
    wex file/createIfNotExists -f="${FILE}"
  fi;

  printf "\n${LINE}" >> "${FILE}"
}
