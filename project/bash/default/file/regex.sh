#!/usr/bin/env bash

fileRegexArgs() {
  _DESCRIPTION='Execute sed in a portable way'
  _ARGUMENTS=(
    'file f "File" true'
    'regex e "Regular expression" true'
  )
}

fileRegex() {
  # Use temp backup file.
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "${REGEX}" "${FILE}"
  # Remove backup file.
  rm "${FILE}${WEX_SED_I_ORIG_EXT}"
}