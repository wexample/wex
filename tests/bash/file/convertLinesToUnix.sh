#!/usr/bin/env bash

fileConvertLinesToUnixTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  wex-exec file/convertLinesToUnix -f="${FILEPATH}"
  _wexTestAssertEqual "$(wex-exec file/getLinesFormat -f="${FILEPATH}")" "LF"
}
