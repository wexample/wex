#!/usr/bin/env bash

varGetTest() {
  local RESULT

  # Clear if present
  wex var/clear -n="testVar"

  # Try to get missing value
  RESULT=$(wex var/get -n="testVar" -d="default value")
  _wexTestAssertEqual "${RESULT}" "default value"

  # Change
  wex var/set -n="testVar" -v="test value"

  # Check
  RESULT=$(wex var/get -n="testVar" -d="default value")
  _wexTestAssertEqual "${RESULT}" "test value"
}
