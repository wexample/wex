#!/usr/bin/env bash

configKeyExistsTest() {
  local FILEPATH
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Normal
  result=$(wex default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")
  _wexTestAssertEqual "${result}" true

  # Commented
  result=$(wex default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -c)
  _wexTestAssertEqual "${result}" true

  # Commented only
  result=$(wex default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -co)
  _wexTestAssertEqual "${result}" true

  # Commented only (after uncomment)
  wex default::config/uncomment -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented"
  result=$(wex default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -co)
  _wexTestAssertEqual "${result}" false

}
