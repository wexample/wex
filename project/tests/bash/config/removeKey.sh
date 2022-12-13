#!/usr/bin/env bash

configRemoveKeyTest() {
  local FILEPATH
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Normal
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")
  _wexTestAssertEqual "${result}" "true"

  wex config/removeKey -f="${FILEPATH}" -k="ConfigTestSingleOption"
  # Normal
  result=$(wex config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")

  _wexTestAssertEqual "${result}" "false"
}
