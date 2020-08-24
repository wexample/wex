#!/usr/bin/env bash

fileTextAppendOnceArgs() {
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
    'create c "Create if exists" false'
  )
}

fileTextAppendOnce() {
  findExactLine=$(wex file/lineExists -f="${FILE}" -l="${LINE}")

  if [ "${findExactLine}" != true ];then
    wex file/textAppend -f="${FILE}" -l="${LINE}" -c="${CREATE}"
  fi
}
