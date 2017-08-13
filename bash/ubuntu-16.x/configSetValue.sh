#!/usr/bin/env bash

configSetValue() {
  TARGET_KEY=${2}
  SEPARATOR=${4}
  FILE=${1}
  VALUE=${3}

  # Prevent empty string
  if [ ${#TARGET_KEY} == 0 ]; then
    return
  fi;

  # Set Value
  # Search for a commented version
  hasValueCommented=$(wexample configKeyExists ${FILE} "${TARGET_KEY}" "${SEPARATOR}" -co)

  if [[ ${hasValueCommented} == true ]];then
    # Uncomment line(s)
    wexample configUncomment ${FILE} "${TARGET_KEY}" "${SEPARATOR}"
  fi;

  # Search for an existing version
  hasValue=$(wexample configKeyExists ${FILE} "${TARGET_KEY}" "${SEPARATOR}")

  if [[ ${hasValue} == true ]];then
    # Change value(s)
    wexample configChangeValue ${FILE} "${TARGET_KEY}" "${VALUE}" "${SEPARATOR}"
  else
    # Add a new line
    wexample fileTextAppendOnce ${FILE} "${TARGET_KEY}${SEPARATOR}${VALUE}"
  fi
}
