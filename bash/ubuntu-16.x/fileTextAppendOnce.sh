#!/usr/bin/env bash

fileTextAppendOnce() {
  FILE="${1}"
  LINE=$(printf "${2}")
  # Escape $ char
  LINE=$(sed -n "s/\\$/\\\\$/p" <<< ${LINE})
  findExactLine=$(wexample fileLineExists ${FILE} "${LINE}")

  if [ "${findExactLine}" != true ]; then
    wexample fileTextAppend "$@"
  fi
}
