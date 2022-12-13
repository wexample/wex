#!/usr/bin/env bash

fileConvertLinesFormatTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex file/convertLinesFormat -f="${FILEPATH}" -t="CRLF"
  wex file/getLinesFormat -f="${FILEPATH}"
}
