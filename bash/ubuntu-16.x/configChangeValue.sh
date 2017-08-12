#!/usr/bin/env bash

configChangeValue() {
  TARGET_KEY=${2}
  SEPARATOR=${4}
  FILE=${1}
  VALUE=${3}

  # Prevent empty string
  if [ ${#TARGET_KEY} == 0 ]; then
    return
  fi;

  if [ -z "${4+x}" ];then
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
