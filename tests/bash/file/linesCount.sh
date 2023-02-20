#!/usr/bin/env bash

fileLinesCountTest() {
  local COUNT
  local FILE_PATH

  FILE_PATH=$(_wexTestSampleInit "fileTextSample1.txt")
  COUNT=$(wex-exec file/linesCount -f="${FILE_PATH}")

  _wexTestAssertEqual "${COUNT}" "20"
}
