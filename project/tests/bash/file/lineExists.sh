#!/usr/bin/env bash

fileLineExistsTest() {
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit "fileTextSample1.txt")

  result=$(wex file/lineExists -f="${FILEPATH}" -l="Sample text with special chars \ / $ !! ? ;)")
  _wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f="${FILEPATH}" -l="[INNER LINE]")
  _wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f="${FILEPATH}" -l="[LAST LINE]")
  _wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f="${FILEPATH}" -l="[FIRST LINE]")
  _wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f="${FILEPATH}" -l="[MISSING LINE]")
  _wexTestAssertEqual "${result}" false

  result=$(wex file/lineExists -f="${FILEPATH}" -l=".*")
  _wexTestAssertEqual "${result}" false
}
