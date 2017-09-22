#!/usr/bin/env bash

configChangeValueTest() {

  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  noSeparator=$(wex config/getValue -f="${filePath}" -k="ConfigTestOption")
  wexampleTestAssertEqual ${noSeparator} "two"

  # Space separator
  configChangeValueTestItem ${filePath} "ConfigTestOption" " "

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
  original=$(wex config/getValue -f="${filePath}" -k="${variableName}" -s="${separator}")

  # Set value.
  wex config/changeValue -f=${filePath} -k=${variableName} -v="${testValue}" -s="${separator}"
  # Get value
  changed=$(wex config/getValue -f="${filePath}" -k="${variableName}" -s="${separator}")
  # Check
  wexampleTestAssertEqual ${changed} "${testValue}"

  # Revert
  wex config/changeValue -f=${filePath} -k=${variableName} -v="${original}" -s="${separator}"
  # Check
  wexampleTestAssertEqual ${changed} "${testValue}"
}
