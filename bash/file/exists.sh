#!/usr/bin/env bash

fileExistsArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileExists() {
  [ -f "${FILE}" ] && echo true || echo false
}
