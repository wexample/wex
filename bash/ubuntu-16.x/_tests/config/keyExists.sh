#!/usr/bin/env bash

configKeyExistsTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  # Normal
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOption")
  wexampleTestAssertEqual "${result}" true

  # Commented
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -c)
  wexampleTestAssertEqual "${result}" true

  # Commented only
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -co)
  wexampleTestAssertEqual "${result}" true

  # Commented only (after uncomment)
  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOptionCommented"
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -co)
  wexampleTestAssertEqual "${result}" false

  # Revert
  git checkout HEAD -- ${filePath}
}
