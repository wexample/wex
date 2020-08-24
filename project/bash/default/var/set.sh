#!/usr/bin/env bash

varSetArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'value v "Variable value" true'
    'file f "Storage file path" false'
    'quotes q "Wrap values into quotes" false true'
  )
}

varSet() {
  # If no file specified
  if [ "${FILE}" = "" ];then
    # Use wex tmp folder
    FILE=${WEX_DIR_TMP}globalVariablesLocalStorage
  fi

  if [ ! -f "${FILE}" ];then
    touch "${FILE}"
  fi

  wex var/clear -n="${NAME}"

  # Remove all previous values.
  wex config/removeKey -k="${NAME}\=" -f="${FILE}"

  # Add double quotes.
  if [ "${QUOTES}" = true ];then
    VALUE="\"${VALUE}\""
  fi

  echo -e "${NAME}=${VALUE}" >> "${FILE}"
}
