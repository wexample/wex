#!/usr/bin/env bash

fileGetLastFilledLineArgs() {
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileGetLastFilledLine() {
  # To linux lines ending
  ORIGINAL=$(wex file/convertLinesToUnix -f=${FILE})
  # Get last line
  echo $(awk '/./{line=$0} END{print line}' ${FILE})
  # Revert lines encoding format.
  wex file/convertLinesFormat -f="${FILE}" -t="${ORIGINAL}"
}
