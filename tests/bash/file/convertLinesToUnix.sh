#!/usr/bin/env bash

fileConvertLinesToUnixTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex file/convertLinesToUnix -f="${FILEPATH}"
  _wexTestAssertEqual "$(wex file/getLinesFormat -f="${FILEPATH}")" "LF"
}
