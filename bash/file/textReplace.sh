#!/usr/bin/env bash

fileTextReplaceArgs() {
  _DESCRIPTION="Replace a text in a file"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'regex r "Regex to apply" true'
    'file f "File" true'
  )
}

fileTextReplace() {
  local ORIGINAL
  # To linux lines ending
  ORIGINAL=$(wex-exec file/convertLinesToUnix -f="${FILE}")
  # Execute common sed
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "${REGEX}" "${FILE}"
  rm "${FILE}${WEX_SED_I_ORIG_EXT}"
  # Revert lines encoding format.
  wex-exec file/convertLinesFormat -f="${FILE}" -t="${ORIGINAL}"
}
