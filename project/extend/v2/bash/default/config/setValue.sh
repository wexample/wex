#!/usr/bin/env bash

configSetValueArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to change" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
   [3]='value v "New value" true'
 )
}

configSetValue() {

  # Set Value
  # Search for a commented version
  hasValueCommented=$(wex config/keyExists -f=${FILE} -k="${TARGET_KEY}" -s="${SEPARATOR}" -co)

  if [ "${hasValueCommented}" == "true" ];then
    # Uncomment line(s)
    wex config/uncomment -f=${FILE} -k="${TARGET_KEY}" -s="${SEPARATOR}"
  fi;

  # Search for an existing version
  hasValue=$(wex config/keyExists -f=${FILE} -k="${TARGET_KEY}" -s="${SEPARATOR}")

  if [[ ${hasValue} == true ]];then
    # Change value(s)
    wex config/changeValue -f=${FILE} -k="${TARGET_KEY}" -v="${VALUE}" -s="${SEPARATOR}"
  else
    # Add a new line
    wex file/textAppendOnce -f=${FILE} -l="${TARGET_KEY}${SEPARATOR}${VALUE}"
  fi
}
