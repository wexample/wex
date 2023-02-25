#!/usr/bin/env bash

fileRemovableArgs() {
  _DESCRIPTION="Return true if path is not a well known risky path"
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
