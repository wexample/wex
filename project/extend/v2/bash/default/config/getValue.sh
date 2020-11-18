#!/usr/bin/env bash

configGetValueArgs() {
  _ARGUMENTS=(
    [0]='target_key k "Target key to get" true'
    [1]='separator s "Separator like space or equal sign, default space" false'
    [2]='file f "File" true'
  )
}

configGetValue() {

  SEPARATOR="$(wex config/processSeparator -s="${SEPARATOR}")"

  # Find a line starting by the key or by some spaces
  # Capture value and auto print it (p option)
  # Sed returns multiple lines in case of multiple entry
  results=$(sed -n "s/^[ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\(.\{0,\}\)/\2/p" ${FILE})

  # As it is a configuration file, take the last value of the variable
  # Which may override the previous values.
  results=${results##*$'\n'}

  # Trim end on lines
  results=$(wex text/trim -t="${results}")

  echo ${results}
}
