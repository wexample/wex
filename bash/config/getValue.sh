#!/usr/bin/env bash

configGetValueArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'target_key k "Target key to get" true'
    'separator s "Separator like space or equal sign, default space" false'
    'file f "File" true'
  )
}

configGetValue() {
  SEPARATOR="$(wex-exec default::config/processSeparator -s="${SEPARATOR}")"

  if [ ! -f "${FILE}" ]; then
    return
  fi

  # Find a line starting by the key or by some spaces
  # Capture value and auto print it (p option)
  # Sed returns multiple lines in case of multiple entry
  RESULTS=$(sed -n "s/^[ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\(.\{0,\}\)/\2/p" "${FILE}")

  # As it is a configuration file, take the last value of the variable
  # Which may override the previous values.
  RESULTS=${RESULTS##*$'\n'}

  # Trim end on lines
  RESULTS=$(wex-exec string/trim -s="${RESULTS}")

  echo "${RESULTS}"
}
