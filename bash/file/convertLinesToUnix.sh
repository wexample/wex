#!/usr/bin/env bash

fileConvertLinesToUnixArgs() {
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileConvertLinesToUnix() {
  # Get original file encoding format.
  ORIGINAL=$(wex-exec file/getLinesFormat -f="${FILE}");
  # Convert to UNIX
  wex-exec file/convertLinesFormat -f="${FILE}" -t=LF
  # Return original format for external usage (revert).
  echo "${ORIGINAL}"
}
