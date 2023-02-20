#!/usr/bin/env bash

fileGetLastFilledLineTest() {
  local FILEPATH
  local LAST_FILLED_LINE

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")
  # Get the last line
  LAST_FILLED_LINE=$(wex-exec file/getLastFilledLine -f="${FILEPATH}")

  # Compare
  _wexTestAssertEqual "${LAST_FILLED_LINE}" "[LAST LINE]"
}
