#!/usr/bin/env bash

fileTextAppendOnceArgs() {
  _DESCRIPTION="Append a line if not exists in file"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
    'create c "Create if exists" false'
  )
}

fileTextAppendOnce() {
  if [ "$(wex-exec file/lineExists -f="${FILE}" -l="${LINE}")" != "true" ]; then
    wex-exec file/textAppend -f="${FILE}" -l="${LINE}" -c="${CREATE}"
  fi
}
