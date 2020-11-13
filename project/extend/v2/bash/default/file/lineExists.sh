#!/usr/bin/env bash

fileLineExistsArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='line l "New line" true'
 )
}

fileLineExists() {
  # To linux lines ending
  ORIGINAL=$(wex file/convertLinesToUnix -f=${FILE})

  # Protect arguments by escaping special chars.
  LINE=$(sed -e 's/[]\/*.^|[]/\\&/g' <<< "${LINE}")
  # Find line.
  results=$(sed -n "s/^\(${LINE}\)$/\1/p" ${FILE})

  if [ "${results}" != "" ]; then
    EXISTS=true
  else
    EXISTS=false
  fi

  echo ${EXISTS}

  # Revert lines encoding format.
  wex file/convertLinesFormat -f=${FILE} -t=${ORIGINAL}
}

