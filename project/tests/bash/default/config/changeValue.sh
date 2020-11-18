#!/usr/bin/env bash

configChangeValueTest() {
  filePath=$(_wexTestSampleInit configSample)

  noSeparator=$(wex config/getValue -f="${filePath}" -k="ConfigTestOption")
  _wexTestAssertEqual ${noSeparator} "two"

  # Space separator
  configChangeValueTestItem ${filePath} "ConfigTestOption" " "

  # Strict equal separator
  configChangeValueTestItem ${filePath} "ConfigTestOptionEqual" "="

  # Revert file.
  filePath=$(_wexTestSampleInit configSample)

  configChangeValueTestItem ${filePath} "ChallengeResponseAuthentication"

  filePath=$(_wexTestSampleInit sshd_config)
  configChangeValueTestItem ${filePath} Port " "
}

configChangeValueTestItem() {
  filePath=${1}
  variableName=${2}
  separator=${3}
  expected="tested"

  # Backup
  original=$(wex config/getValue -f="${filePath}" -k="${variableName}" -s="${separator}")

  # Set value.
  wex config/changeValue -f=${filePath} -k=${variableName} -v="${expected}" -s="${separator}"
  # Get value
  changed=$(wex config/getValue -f="${filePath}" -k="${variableName}" -s="${separator}")
  # Check
  _wexTestAssertEqual "${changed}" "${expected}"

  # Revert
  wex config/changeValue -f=${filePath} -k=${variableName} -v="${original}" -s="${separator}"
  # Get value
  changed=$(wex config/getValue -f="${filePath}" -k="${variableName}" -s="${separator}")
  # Check
  _wexTestAssertEqual "${changed}" "${original}"
}
