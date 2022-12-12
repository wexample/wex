#!/usr/bin/env bash

configKeyExistsTest() {
  local FILEPATH
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Normal
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")
  _wexTestAssertEqual "${result}" true

  # Commented
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -c)
  _wexTestAssertEqual "${result}" true

  # Commented only
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -co)
  _wexTestAssertEqual "${result}" true

  # Commented only (after uncomment)
  wex config/uncomment -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented"
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -co)
  _wexTestAssertEqual "${result}" false

}
