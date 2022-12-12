#!/usr/bin/env bash

phpConstantChangeTest() {
  local FILE_PATH
  # Revert file.
  FILE_PATH=$(_wexTestSampleInit sample.php)

  original=$(< ${filePath})

  wex php/constantChange -f="${FILE_PATH}" -k=TEST_VAR_ONE -v=tested
  _wexTestSampleDiff sample.php true "VAR_ONE changed"

  wex php/constantChange -f="${FILE_PATH}" -k=TEST_VAR_TWO -v=tested
  _wexTestSampleDiff sample.php true "VAR_TWO changed"

  wex php/constantChange -f="${FILE_PATH}" -k=TEST_VAR_ONE -v=one
  wex php/constantChange -f="${FILE_PATH}" -k=TEST_VAR_TWO -v=two
  _wexTestSampleDiff sample.php false "vars rollback"
}
