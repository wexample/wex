#!/usr/bin/env bash

configKeyExistsTest() {
  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Normal
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOption")
  wexTestAssertEqual "${result}" true

  # Commented
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -c)
  wexTestAssertEqual "${result}" true

  # Commented only
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -co)
  wexTestAssertEqual "${result}" true

  # Commented only (after uncomment)
  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOptionCommented"
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOptionCommented" -co)
  wexTestAssertEqual "${result}" false

}
