#!/usr/bin/env bash

configChangeValueArgs() {
  _DESCRIPTION="Change a value of a key / value pair in a config file"
  _ARGUMENTS=(
    'target_key k "Target key to change" true'
    'separator s "Separator like space or equal sign, default space" false'
    'file f "File" true'
    'value v "New value" true'
  )
}

configChangeValue() {
  SEPARATOR="$(wex config/processSeparator -s="${SEPARATOR}")"

  # Escape string.
  VALUE=$(echo "${VALUE}" | sed 's/\//\\\//g')
  TARGET_KEY=$(echo "${TARGET_KEY}" | sed 's/\//\\\//g')
  # Find a line starting by the key or by some spaces, and capture it
  # Commented lines are ignored.
  # Change all occurrences if multiple.
  wex file/regex -f ${FILE} -e "s/^\([ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)\(.\{0,\}\)/\1${VALUE}/"
}
