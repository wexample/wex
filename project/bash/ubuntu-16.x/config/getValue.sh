#!/usr/bin/env bash

configGetValueArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to get" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
 )
}

configGetValue() {

  if [ -z "${SEPARATOR+x}" ];then
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
