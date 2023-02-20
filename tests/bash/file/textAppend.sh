#!/usr/bin/env bash

fileTextAppendTest() {
  local FILEPATH
  local TEST_TEXT

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")
  TEST_TEXT="Hey this is a test"

  wex-exec file/textAppend -f="${FILEPATH}" -l="${TEST_TEXT}"
  # Get the last line
  fileGetLastFilledLine=$(wex-exec file/getLastFilledLine -f="${FILEPATH}")
  # Compare
  _wexTestAssertEqual "${fileGetLastFilledLine}" "${TEST_TEXT}"

  # Cleanup
  wex-exec file/textRemoveLastLine -f="${FILEPATH}"

  # Check las line removed.
  fileGetLastFilledLine=$(wex-exec file/getLastFilledLine -f="${FILEPATH}")
  # Compare
  _wexTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
}
