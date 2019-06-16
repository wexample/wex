#!/usr/bin/env bash

phpConstantChangeTest() {

  # Revert file.
  filePath=$(wexTestSampleInit sample.php)

  original=$(< ${filePath})

  wex php/constantChange -f=${filePath} -k=TEST_VAR_ONE -v=tested
  wexTestSampleDiff sample.php true "VAR_ONE changed"

  wex php/constantChange -f=${filePath} -k=TEST_VAR_TWO -v=tested
  wexTestSampleDiff sample.php true "VAR_TWO changed"

  wex php/constantChange -f=${filePath} -k=TEST_VAR_ONE -v=one
  wex php/constantChange -f=${filePath} -k=TEST_VAR_TWO -v=two
  wexTestSampleDiff sample.php false "vars rollback"
}
