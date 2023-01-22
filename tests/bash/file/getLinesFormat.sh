#!/usr/bin/env bash

fileGetLinesFormatTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex file/convertLinesFormat -f="${FILEPATH}" -t="LF"
  _wexTestAssertEqual "$(wex file/getLinesFormat -f="${FILEPATH}")" "LF"
}
