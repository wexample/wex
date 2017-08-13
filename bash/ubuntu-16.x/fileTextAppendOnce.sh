#!/usr/bin/env bash

fileTextAppendOnce() {
  FILE="${1}"
  LINE=$(printf "${2}")

  # Protect arguments, escape \, $
  LINE=$(sed 's/\\/\\\\/g' <<< "${LINE}")
  LINE=$(sed 's/\//\\\//g' <<< "${LINE}")
  LINE=$(sed 's/\$/\\$/g' <<< "${LINE}")

  findExactLine=$(wexample fileLineExists ${FILE} "${LINE}")

  if [ "${findExactLine}" != true ]; then
    wexample fileTextAppend ${FILE} "${LINE}"
  fi
}
