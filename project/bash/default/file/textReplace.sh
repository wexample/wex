#!/usr/bin/env bash

fileTextReplaceArgs() {
  _ARGUMENTS=(
    [0]='regex r "Regex to apply" true'
    [1]='file f "File" true'
  )
}

fileTextReplace() {
  # To linux lines ending
  ORIGINAL=$(wex file/convertLinesToUnix -f=${FILE})
  # Execute common sed
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "${REGEX}" ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
  # Revert lines encoding format.
  wex file/convertLinesFormat -f=${FILE} -t=${ORIGINAL}
}
