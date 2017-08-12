#!/usr/bin/env bash

configGetValue() {
  TARGET_KEY=${2}
  SEPARATOR=${3}
  FILE=${1}

  # Prevent empty string
  if [ ${#TARGET_KEY} == 0 ]; then
    return
  fi;

  if [ -z "${3+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Find a line starting by the key or by some spaces
  # Capture value and auto print it (p option)
  # Sed returns multiple lines in case of multiple entry
  results=$(sed -n "s/^[ ]*${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\(.*\)/\1/p" ${FILE})

  # As it is a configuration file, take the last value of the variable
  # Which may override the previous values.
  echo ${results##*$'\n'}
}
