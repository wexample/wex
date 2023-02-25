#!/usr/bin/env bash

fileCreateIfNotExistsArgs() {
  _DESCRIPTION="Create e file in not exists"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileCreateIfNotExists() {
  if [ "$(wex-exec file/exists -f="${FILE}")" = false ]; then
    touch "${FILE}"
  fi
}
