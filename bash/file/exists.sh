#!/usr/bin/env bash

fileExistsArgs() {
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileExists() {
  [[ -f "${FILE}" ]] && echo true || echo false
}
