#!/usr/bin/env bash

fileRemoveArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Remove a file or directory if it exists and not a root directory."
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileRemove() {
  if [[ $(wex-exec file/removable -f="${FILE}") == true ]]; then
    rm -rf "${FILE}"
  fi
}
