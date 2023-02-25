#!/usr/bin/env bash

fileTextRemoveLastLineArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileTextRemoveLastLine() {
  head -n -1 "${FILE}" >"${FILE}".tmp
  mv "${FILE}".tmp "${FILE}"
}
