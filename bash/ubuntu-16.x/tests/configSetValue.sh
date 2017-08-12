#!/usr/bin/env bash

configSetValueTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  # Existing option
  wexample configSetValue "${filePath}" "ConfigTestOption" "testValue"
  # Get changed value.
  value=$(wexample configGetValue ${filePath} "ConfigTestOption")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option
  wexample configSetValue "${filePath}" "ConfigTestSingleOptionCommented" "testValue"
  # Get changed value.
  value=$(wexample configGetValue ${filePath} "ConfigTestSingleOptionCommented")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option with equal separator
  wexample configSetValue "${filePath}" "ConfigTestSingleOptionCommentedWithEqual" "testValue" "="
  # Get changed value.
  value=$(wexample configGetValue ${filePath} "ConfigTestSingleOptionCommentedWithEqual" "=")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}

  # Commented option with equal separator
  wexample configSetValue "${filePath}" "ConfigTestMissingOption" "testValue" "="
  # Get changed value.
  value=$(wexample configGetValue ${filePath} "ConfigTestMissingOption" "=")
  # Check
  wexampleTestAssertEqual ${value} "testValue"
  # Revert
  git checkout HEAD -- ${filePath}
}
