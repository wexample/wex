#!/usr/bin/env bash

fileGetLastFilledLineTest() {
  filePath=$(wexTestSampleInit "fileTextSample1.txt")
  # Get the last line
  fileGetLastFilledLine=$(wex file/getLastFilledLine -f=${filePath})
  # Compare
  wexTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
}
