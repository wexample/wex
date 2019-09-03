#!/usr/bin/env bash

stringTrimArgs() {
  _DESCRIPTION="Trim a string"
  _ARGUMENTS=(
    'string s "String to trim" true'
  )
}

stringTrim() {
  echo -e "${STRING}" | sed -e 's/^[[:space:]]\{0,\}//' -e 's/[[:space:]]\{0,\}$//'
}
