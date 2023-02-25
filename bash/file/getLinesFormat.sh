#!/usr/bin/env bash

fileGetLinesFormatArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileGetLinesFormat() {
  if [[ $(file -b - <"${FILE}") =~ CRLF ]]; then
    echo "CRLF"
  elif [[ $(file -b - <"${FILE}") =~ CR ]]; then
    echo "CR"
  else
    echo "LF"
  fi
}
