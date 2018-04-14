#!/usr/bin/env bash

varIsNumberArgs() {
  _ARGUMENTS=(
    [0]='variable v "Variable content to test" true'
  )
}

varIsNumber() {
  # Is number ?
  if [[ ${VARIABLE} =~ ^-?[0-9]+$ ]]; then
    echo true
  else
    echo false
  fi
}
