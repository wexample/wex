#!/usr/bin/env bash

configSetValueTest() {
  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Existing option
  wex config/setValue -f="${filePath}" -k="ConfigTestOption" -v="testValue"
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOption")
  # Check
  wexTestAssertEqual ${value} "testValue"

  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Commented option
  wex config/setValue -f="${filePath}" -k="ConfigTestSingleOptionCommented" -v="testValue"
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestSingleOptionCommented")
  # Check
  wexTestAssertEqual ${value} "testValue"

  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Commented option with equal separator
  wex config/setValue -f="${filePath}" -k="ConfigTestSingleOptionCommentedWithEqual" -v="testValue" -s="="
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestSingleOptionCommentedWithEqual" -s="=")
  # Check
  wexTestAssertEqual ${value} "testValue"

  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Commented option with equal separator
  wex config/setValue -f="${filePath}" -k="ConfigTestMissingOption" -v="testValue" -s="="
  # Get changed value.
  value=$(wex config/getValue -f=${filePath} -k="ConfigTestMissingOption" -s="=")
  # Check
  wexTestAssertEqual ${value} "testValue"
}
