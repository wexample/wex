#!/usr/bin/env bash

configRemoveKeyTest() {
  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Normal
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOption")
  wexTestAssertEqual "${result}" "true"

  wex config/removeKey -f=${filePath} -k="ConfigTestSingleOption"
  # Normal
  result=$(wex config/keyExists -f=${filePath} -k="ConfigTestSingleOption")

  wexTestAssertEqual "${result}" "false"
}
