#!/usr/bin/env bash

fileRemoveArgs() {
  _DESCRIPTION="Remove a file or directory if it exists and not a root directory."
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileRemove() {
  if [[ $(wex file/removable -f="${FILE}") == true ]]; then
    rm -rf "${FILE}"
  fi
}
