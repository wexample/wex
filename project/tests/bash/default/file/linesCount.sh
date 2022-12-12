#!/usr/bin/env bash

fileLinesCountTest() {
  local FILE_PATH=$(_wexTestSampleInit "fileTextSample1.txt")
  local COUNT=$(wex file/linesCount -f=${FILE_PATH})
  _wexTestAssertEqual "${COUNT}" "20"
}
