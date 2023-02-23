#!/usr/bin/env bash

fileRemovableArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileRemovable() {
  if [ -n "${FILE}" ] && [ -e "${FILE}" ] && [[ ! "${FILE}" =~ ^/ ]]; then
    echo true
  else
    echo false
  fi
}
