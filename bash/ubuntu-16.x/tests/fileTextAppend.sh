#!/usr/bin/env bash

fileTextAppendTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt
  testText="Hey this is a test"
  wexample fileTextAppend ${filePath} "${testText}"
  # Get the last line
  fileGetLastFilledLine=$(wexample fileGetLastFilledLine ${filePath})
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "${testText}"
  # Cleanup
  wexample fileTextRemoveLastLine ${filePath}
  # Check las line removed.
  fileGetLastFilledLine=$(wexample fileGetLastFilledLine ${filePath})
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
  # Revert file in order to avoid git conflicts.
  git checkout HEAD -- ${filePath}
}
