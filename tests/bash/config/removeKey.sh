#!/usr/bin/env bash

configRemoveKeyTest() {
  local FILEPATH
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Normal
  result=$(wex-exec default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")
  _wexTestAssertEqual "${result}" "true"

  wex-exec default::config/removeKey -f="${FILEPATH}" -k="ConfigTestSingleOption"
  # Normal
  result=$(wex-exec default::config/keyExists -f="${FILEPATH}" -k="ConfigTestSingleOption")

  _wexTestAssertEqual "${result}" "false"
}
