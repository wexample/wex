#!/usr/bin/env bash

configSetValueArgs() {
 _ARGUMENTS=(
   'key k "Target key to change" true'
   'separator s "Separator like space or equal sign, default space" false " "'
   'file f "File" true'
   'ignore_duplicates i "Do not check if variable exists or is commented" false'
   'value v "New value" true'
 )
}

configSetValue() {
  _wexItem "${KEY}=" "${VALUE}" "    > $(basename ${FILE}) "

  if [ "${IGNORE_DUPLICATES}" = "true" ];then
    # Add value without checks.
    echo -e "${KEY}${SEPARATOR}${VALUE}" >> ${FILE}
    return
  fi

  local HAS_VALUE;

  # Set Value
  # Search for a commented version
  local HAS_VALUE_COMMENTED=$(wex config/keyExists -f=${FILE} -k="${KEY}" -s="${SEPARATOR}" -co)

  if [ "${HAS_VALUE_COMMENTED}" = "true" ];then
    # Uncomment line(s)
    wex config/uncomment -f=${FILE} -k="${KEY}" -s="${SEPARATOR}"
    HAS_VALUE=true
  else
    # Search for an existing version
    HAS_VALUE=$(wex config/keyExists -f=${FILE} -k="${KEY}" -s="${SEPARATOR}")
  fi;

  if [ "${HAS_VALUE}" = "true" ];then
    # Change value(s)
    wex config/changeValue -f=${FILE} -k="${KEY}" -v="${VALUE}" -s="${SEPARATOR}"
  else
    # Add a new line
    wex file/textAppendOnce -f=${FILE} -l="${KEY}${SEPARATOR}${VALUE}"
  fi
}
