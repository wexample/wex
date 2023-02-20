#!/usr/bin/env bash

configSetValueTest() {
  local FILEPATH
  local VALUE
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Existing option
  wex-exec default::config/setValue -f="${FILEPATH}" -k="ConfigTestOption" -v="testValue"
  # Get changed value.
  VALUE=$(wex-exec default::config/getValue -f="${FILEPATH}" -k="ConfigTestOption")
  # Check
  _wexTestAssertEqual "${VALUE}" "testValue"

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Commented option
  wex-exec default::config/setValue -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented" -v="testValue"
  # Get changed value.
  VALUE=$(wex-exec default::config/getValue -f="${FILEPATH}" -k="ConfigTestSingleOptionCommented")
  # Check
  _wexTestAssertEqual "${VALUE}" "testValue"

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Commented option with equal separator
  wex-exec default::config/setValue -f="${FILEPATH}" -k="ConfigTestSingleOptionCommentedWithEqual" -v="testValue" -s="="
  # Get changed value.
  VALUE=$(wex-exec default::config/getValue -f="${FILEPATH}" -k="ConfigTestSingleOptionCommentedWithEqual" -s="=")
  # Check
  _wexTestAssertEqual "${VALUE}" "testValue"

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Commented option with equal separator
  wex-exec default::config/setValue -f="${FILEPATH}" -k="ConfigTestMissingOption" -v="testValue" -s="="
  # Get changed value.
  VALUE=$(wex-exec default::config/getValue -f="${FILEPATH}" -k="ConfigTestMissingOption" -s="=")
  # Check
  _wexTestAssertEqual "${VALUE}" "testValue"
}
