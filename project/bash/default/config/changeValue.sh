#!/usr/bin/env bash

configChangeValueArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to change" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
   [3]='value v "New value" true'
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
  sed -i "s/^\([ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)\(.\{0,\}\)/\1${VALUE}/" ${FILE}
}
