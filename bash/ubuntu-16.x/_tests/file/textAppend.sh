#!/usr/bin/env bash

fileTextAppendTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt
  testText="Hey this is a test"
  wex file/textAppend -f=${filePath} -l="${testText}"
  # Get the last line
  fileGetLastFilledLine=$(wex file/getLastFilledLine -f=${filePath})
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "${testText}"
  # Cleanup
  wex file/textRemoveLastLine -f=${filePath}
  # Check las line removed.
  fileGetLastFilledLine=$(wex file/getLastFilledLine -f=${filePath})
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
  # Revert file in order to avoid git conflicts.
  git checkout HEAD -- ${filePath}
}
