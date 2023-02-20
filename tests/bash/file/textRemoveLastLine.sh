#!/usr/bin/env bash

fileTextRemoveLastLineTest() {
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  _wexTestAssertEqual "$(wex-exec default::config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" 'yes'

  wex-exec file/textRemoveLastLine -f="${FILEPATH}"

  # No more value
  _wexTestAssertEqual "$(wex-exec default::config/getValue -f="${FILEPATH}" -k="UsePAM" -s=" ")" ""
}
