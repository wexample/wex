#!/usr/bin/env bash

fileTextRemoveLastLineTest() {
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  _wexTestAssertEqual "$(wex default::config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" 'yes'

  wex file/textRemoveLastLine -f="${FILEPATH}"

  # No more value
  _wexTestAssertEqual "$(wex default::config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" ""
}
