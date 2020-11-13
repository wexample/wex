#!/usr/bin/env bash

fileLinesCountTest() {
  filePath=$(wexTestSampleInit "fileTextSample1.txt")
  local count=$(wex file/linesCount -f=${filePath})
  wexTestAssertEqual "${count}" "20"
}
