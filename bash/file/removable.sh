#!/usr/bin/env bash

fileRemovableArgs() {
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
