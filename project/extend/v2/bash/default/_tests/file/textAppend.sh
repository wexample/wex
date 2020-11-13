#!/usr/bin/env bash

fileTextAppendTest() {
  filePath=$(wexTestSampleInit "fileTextSample1.txt")
  testText="Hey this is a test"
  wex file/textAppend -f=${filePath} -l="${testText}"
  # Get the last line
  fileGetLastFilledLine=$(wex file/getLastFilledLine -f=${filePath})
  # Compare
  wexTestAssertEqual "${fileGetLastFilledLine}" "${testText}"
  # Cleanup
  wex file/textRemoveLastLine -f=${filePath}
  # Check las line removed.
  fileGetLastFilledLine=$(wex file/getLastFilledLine -f=${filePath})
  # Compare
  wexTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
}
