#!/usr/bin/env bash

fileLineExistsArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
   'file f "File" true'
   'line l "New line" true'
 )
}

fileLineExists() {
  local ORIGINAL
  # To linux lines ending
  ORIGINAL=$(wex-exec file/convertLinesToUnix -f="${FILE}")

  # Protect arguments by escaping special chars.
  LINE=$(sed -e 's/[]\/*.^|[]/\\&/g' <<< "${LINE}")
  # Find line.
  results=$(sed -n "s/^\(${LINE}\)$/\1/p" "${FILE}")

  if [ "${results}" != "" ]; then
    EXISTS=true
  else
    EXISTS=false
  fi

  echo ${EXISTS}

  # Revert lines encoding format.
  wex-exec file/convertLinesFormat -f="${FILE}" -t="${ORIGINAL}"
}

