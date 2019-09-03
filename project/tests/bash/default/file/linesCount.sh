#!/usr/bin/env bash

fileLinesCountTest() {
  local filePath=$(_wexTestSampleInit "fileTextSample1.txt")
  local count=$(wex file/linesCount -f=${filePath})
  _wexTestAssertEqual "${count}" "20"
}
