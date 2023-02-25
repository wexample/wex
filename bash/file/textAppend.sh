#!/usr/bin/env bash

fileTextAppendArgs() {
  _DESCRIPTION="Append a line to the end of file"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
    'create c "Create if exists" false'
  )
}

fileTextAppend() {
  if [ "${CREATE}" = "true" ]; then
    wex-exec file/createIfNotExists -f="${FILE}"
  fi

  printf "\n${LINE}" >>"${FILE}"
}
