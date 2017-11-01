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

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Escape string.
  VALUE=$(echo "${VALUE}" | sed 's/\//\\\//g')
  TARGET_KEY=$(echo "${TARGET_KEY}" | sed 's/\//\\\//g')
  # Find a line starting by the key or by some spaces, and capture it
  # Commented lines are ignored.
  # Change all occurrences if multiple.
  sed -i "s/^\([ ]*${TARGET_KEY}[ ]*[${SEPARATOR}]\+[ ]*\)\(.*\)/\1${VALUE}/" ${FILE}
}
