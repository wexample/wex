#!/usr/bin/env bash

fileExistsTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  _wexTestAssertEqual "$(wex-exec file/exists -f="${FILEPATH}")" "true"

  _wexTestAssertEqual "$(wex-exec file/exists -f="${FILEPATH}missingFile")" "false"
}
