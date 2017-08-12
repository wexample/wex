#!/usr/bin/env bash

fileTextReplace() {
  REGEX=${1}
  FILE=${2}
  # Get original file encoding format.
  lineEncodingFormatOriginal=$(wexample fileGetLinesFormat ${FILE});
  # Execute common sed
  sed -i "${REGEX}" ${FILE}
  # Revert lines encoding format.
  wexample fileConvertLinesFormat ${FILE} ${lineEncodingFormatOriginal}
}
