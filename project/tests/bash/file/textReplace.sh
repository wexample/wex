#!/usr/bin/env bash

fileTextReplaceTest() {
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  # Replace
  wex file/textReplace -f="${FILEPATH}" -r="s/prohibit-password/yolo/"

  # Test change
  _wexTestAssertEqual $(wex config/getValue -f="${FILEPATH}" -k="PermitRootLogin") 'yolo'
}
