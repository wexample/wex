#!/usr/bin/env bash

configSetValueArgs() {
 _ARGUMENTS=(
   'key k "Target key to change" true'
   'separator s "Separator like space or equal sign, default space" false " "'
   'file f "File" true'
   'ignore_duplicates i "Do not check if variable exists or is commented" false false'
   'value v "New value" true'
 )
}

configSetValue() {
  # Empty separator
  if [ "${SEPARATOR}" = "" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  if [ "${IGNORE_DUPLICATES}" = "true" ];then
    # Add value without checks.
    echo -e "\n${KEY}${SEPARATOR}${VALUE}" >> "${FILE}"
    return
  fi

  local HAS_VALUE;
  local HAS_VALUE_COMMENTED

  # Set Value
  # Search for a commented version
  HAS_VALUE_COMMENTED=$(wex config/keyExists -f="${FILE}" -k="${KEY}" -s="${SEPARATOR}" -co)

  if [ "${HAS_VALUE_COMMENTED}" = "true" ];then
    # Uncomment line(s)
    wex config/uncomment -f="${FILE}" -k="${KEY}" -s="${SEPARATOR}"
    HAS_VALUE=true
  else
    # Search for an existing version
    HAS_VALUE=$(wex config/keyExists -f="${FILE}" -k="${KEY}" -s="${SEPARATOR}")
  fi;

  if [ "${HAS_VALUE}" = "true" ];then
    # Change value(s)
    wex config/changeValue -f="${FILE}" -k="${KEY}" -v="${VALUE}" -s="${SEPARATOR}"
  else
    # Add a new line
    wex file/textAppendOnce -f="${FILE}" -l="\n${KEY}${SEPARATOR}${VALUE}"
  fi
}
