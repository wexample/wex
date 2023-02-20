#!/usr/bin/env bash

stringSplitTest() {
  local ARRAY
  # See : https://github.com/koalaman/shellcheck/wiki/SC2207
  local ARRAY_SPLIT_COMMAND="mapfile -t ARRAY"

  ${ARRAY_SPLIT_COMMAND} < <(wex-exec default::string/split -t="one,two,three")
  _wexTestAssertEqual "${ARRAY[1]}" "two"

  ${ARRAY_SPLIT_COMMAND} < <(wex-exec default::string/split -t="the first.the second.the third" -s=".")
  _wexTestAssertEqual "${ARRAY[1]}" "the second"
}
