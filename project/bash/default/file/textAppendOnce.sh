#!/usr/bin/env bash

fileTextAppendOnceArgs() {
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
    'create c "Create if exists" false'
  )
}

fileTextAppendOnce() {
  if [ "$(wex file/lineExists -f="${FILE}" -l="${LINE}")" != "true" ];then
    wex file/textAppend -f="${FILE}" -l="${LINE}" -c="${CREATE}"
  fi
}
