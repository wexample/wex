#!/usr/bin/env bash

configGetValueTest() {
  local FILEPATH
  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  value=$(wex config/getValue -f="${FILEPATH}" -k="ConfigTestOption")
  # Got the last valid value
  _wexTestAssertEqual "${value}" "two"

  value=$(wex config/getValue -f="${FILEPATH}" -k="ConfigTestOptionEqual" -s=" = ")
  _wexTestAssertEqual "${value}" "one"

  value=$(wex config/getValue -f="${FILEPATH}" -k="ConfigTestOptionEqual" -s="=")
  # Got the last valid value
  _wexTestAssertEqual "${value}" "two"
}
