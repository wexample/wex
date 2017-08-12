#!/usr/bin/env bash

configKeyExistsTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  # Normal
  result=$(wexample configKeyExists ${filePath} "ConfigTestSingleOption")
  wexampleTestAssertEqual "${result}" true

  # Commented
  result=$(wexample configKeyExists ${filePath} "ConfigTestSingleOptionCommented" -c)
  wexampleTestAssertEqual "${result}" true

  # Commented only
  result=$(wexample configKeyExists ${filePath} "ConfigTestSingleOptionCommented" -co)
  wexampleTestAssertEqual "${result}" true

  # Commented only (after uncomment)
  wexample configUncomment ${filePath} "ConfigTestSingleOptionCommented"
  result=$(wexample configKeyExists ${filePath} "ConfigTestSingleOptionCommented" -co)
  wexampleTestAssertEqual "${result}" false

  # Revert
  git checkout HEAD -- ${filePath}
}
