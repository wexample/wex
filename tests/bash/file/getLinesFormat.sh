#!/usr/bin/env bash

fileGetLinesFormatTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex-exec file/convertLinesFormat -f="${FILEPATH}" -t="LF"
  _wexTestAssertEqual "$(wex-exec file/getLinesFormat -f="${FILEPATH}")" "LF"
}
