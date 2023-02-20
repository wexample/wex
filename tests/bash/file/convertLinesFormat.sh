#!/usr/bin/env bash

fileConvertLinesFormatTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex-exec file/convertLinesFormat -f="${FILEPATH}" -t="CRLF"
  wex-exec file/getLinesFormat -f="${FILEPATH}"
}
