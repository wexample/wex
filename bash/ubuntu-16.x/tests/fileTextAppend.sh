#!/usr/bin/env bash

fileTextAppendTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt
  testText="Hey this is a test"
  wexample fileTextAppend ${filePath} "${testText}"
  # Get the last line
  fileGetLastFilledLine=$(wexample fileGetLastFilledLine "${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt")
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "${testText}"
  # Cleanup
  wexample fileTextRemoveLastLine "${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt"
  # Check las line removed.
  fileGetLastFilledLine=$(wexample fileGetLastFilledLine "${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt")
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
}
