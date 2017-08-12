#!/usr/bin/env bash

configChangeValueTest() {

  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  # Space separator
  configChangeValueTestItem ${filePath} "ConfigTestOption"

  # Strict equal separator
  configChangeValueTestItem ${filePath} "ConfigTestOptionEqual" "="

  # Revert file in order to avoid git conflicts.
  git checkout HEAD -- ${filePath}

  filePath=${_TEST_RUN_DIR_SAMPLES}configSample
  configChangeValueTestItem ${filePath} "ChallengeResponseAuthentication"

  # Revert file in order to avoid git conflicts.
  git checkout HEAD -- ${filePath}
}

configChangeValueTestItem() {
  filePath=${1}
  variableName=${2}
  separator=${3}
  testValue="tested"

  # Backup
  original=$(wexample configGetValue "${filePath}" "${variableName}" "${separator}")

  # Set value.
  wexample configChangeValue "${filePath}" "${variableName}" "${testValue}" "${separator}"
  # Get value
  changed=$(wexample configGetValue "${filePath}" "${variableName}" "${separator}")
  # Check
  wexampleTestAssertEqual ${changed} "${testValue}"

  # Revert
  wexample configChangeValue "${filePath}" "${variableName}" "${original}" "${separator}"
  # Check
  wexampleTestAssertEqual ${changed} "${testValue}"
}
