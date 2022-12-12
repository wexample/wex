#!/usr/bin/env bash

systemPathAddTest() {
  local COMMAND
  local FILEPATH
  local NEW_PATH

  NEW_PATH=/toto/tata

  FILEPATH=$(_wexTestSampleInit bashrc)
  COMMAND=$(wex system/pathAdd -p=${NEW_PATH} -b="${FILEPATH}" -g="Lorem ipsum")
  _wexTestSampleDiff bashrc true "Command added to test bashrc file"

  _wexTestAssertNotEmpty "${COMMAND}"

  FILEPATH=$(_wexTestSampleInit bashrc)
  # Exactly the same command with another PATH content
  COMMAND=$(wex system/pathAdd -p=${NEW_PATH} -b="${FILEPATH}" -g="Lorem ipsum:${NEW_PATH}")
  _wexTestSampleDiff bashrc true "Second command added to test bashrc file"
  _wexTestAssertNotEmpty "${COMMAND}"
}
