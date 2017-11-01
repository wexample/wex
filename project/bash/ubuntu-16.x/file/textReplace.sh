#!/usr/bin/env bash

fileTextReplaceArgs() {
 _ARGUMENTS=(
   [0]='regex r "Regex to apply" true'
   [1]='file f "File" true'
 )
}

fileTextReplace() {
  # Get original file encoding format.
  lineEncodingFormatOriginal=$(wex file/getLinesFormat -f=${FILE});
  # Execute common sed
  sed -i "${REGEX}" ${FILE}
  # Revert lines encoding format.
  wex file/convertLinesFormat -f=${FILE} -t=${lineEncodingFormatOriginal}
}
