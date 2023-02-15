#!/usr/bin/env bash

arraySortTest() {
  local ARRAY=(aa cc bb)

  _wexTestAssertEqual "${ARRAY[2]}" "bb"

  ARRAY=($(wex array/sort -a="${ARRAY[*]}" -s=" "))

  _wexTestAssertEqual "${ARRAY[2]}" "cc"
}

