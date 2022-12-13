#!/usr/bin/env bash

fileTextRemoveLastLineTest() {
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  _wexTestAssertEqual "$(wex config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" 'yes'

  wex file/textRemoveLastLine -f="${FILEPATH}"

  # No more value
  _wexTestAssertEqual "$(wex config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" ""
}
