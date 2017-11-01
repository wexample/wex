#!/usr/bin/env bash

fileLineExistsArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='line l "New line" true'
 )
}

fileLineExists() {
  # Protect arguments by escaping special chars.
  LINE=$(sed -e 's/[]\/$*.^|[]/\\&/g' <<< "${LINE}")
  # Find line.
  results=$(sed -n "s/^\(${LINE}\)$/\1/p" ${FILE})

  if [ "${results}" != "" ]; then
    echo true
    return
  fi

  echo false
}

