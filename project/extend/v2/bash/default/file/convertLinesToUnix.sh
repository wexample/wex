#!/usr/bin/env bash

fileConvertLinesToUnixArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
  )
}

fileConvertLinesToUnix() {
  # Get original file encoding format.
  ORIGINAL=$(wex file/getLinesFormat -f=${FILE});
  # Convert to UNIX
  wex file/convertLinesFormat -f=${FILE} -t=LF
  # Return original format for external usage (revert).
  echo ${ORIGINAL}
}
