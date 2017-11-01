#!/usr/bin/env bash

configSetValueTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  # Existing option
  wex config/setValue -f="${filePath}" -k="ConfigTestOption" -v="testValue"
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOption")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option
  wex config/setValue -f="${filePath}" -k="ConfigTestSingleOptionCommented" -v="testValue"
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestSingleOptionCommented")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option with equal separator
  wex config/setValue -f="${filePath}" -k="ConfigTestSingleOptionCommentedWithEqual" -v="testValue" -s="="
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestSingleOptionCommentedWithEqual" -s="=")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option with equal separator
  wex config/setValue -f="${filePath}" -k="ConfigTestMissingOption" -v="testValue" -s="="
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestMissingOption" -s="=")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
#  git checkout HEAD -- ${filePath}
}
