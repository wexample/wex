#!/usr/bin/env bash

configUncommentTest() {
  local FILEPATH
  local VALUE

  FILEPATH=$(_wexTestSampleInit configSample)

  wex default::config/uncomment -f="${FILEPATH}" -k="KerberosGetAFSToken"
  VALUE=$(wex default::config/getValue -f="${FILEPATH}" -k="KerberosGetAFSToken" -s=" ")

  _wexTestAssertEqual "${VALUE}" "no"
}
