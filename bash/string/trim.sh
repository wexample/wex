#!/usr/bin/env bash

stringTrimArgs() {
  _DESCRIPTION="Trim a string"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'string s "String to trim" true'
    'char c "Char to trim" true " \t"'
  )
}

stringTrim() {
  echo "${STRING}" | sed -e 's/^['"${CHAR}"']*//' | sed -e 's/['"${CHAR}"']*$//'
}
