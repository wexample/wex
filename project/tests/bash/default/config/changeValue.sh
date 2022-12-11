#!/usr/bin/env bash

configChangeValueTest() {
  local RESULT
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  RESULT=$(wex config/processSeparator -s=",")
  _wexTestAssertEqual "${RESULT}" "\(,\)\{1,\}"

  # No separator
  RESULT=$(wex config/getValue -f="${FILEPATH}" -k="ConfigTestOption")
  _wexTestAssertEqual "${RESULT}" "two"

  # Space separator
  configChangeValueTestItem "${FILEPATH}" "ConfigTestOption" " "

  # Strict equal separator
  configChangeValueTestItem "${FILEPATH}" "ConfigTestOptionEqual" "="

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  configChangeValueTestItem "${FILEPATH}" "ChallengeResponseAuthentication"

  FILEPATH=$(_wexTestSampleInit sshd_config)
  configChangeValueTestItem "${FILEPATH}" Port " "
}

configChangeValueTestItem() {
  FILEPATH=${1}
  variableName=${2}
  separator=${3}
  expected="tested"

  # Backup
  original=$(wex config/getValue -f="${FILEPATH}" -k="${variableName}" -s="${separator}")

  # Set value.
  wex config/changeValue -f=${FILEPATH} -k=${variableName} -v="${expected}" -s="${separator}"
  # Get value
  changed=$(wex config/getValue -f="${FILEPATH}" -k="${variableName}" -s="${separator}")
  # Check
  _wexTestAssertEqual "${changed}" "${expected}"

  # Revert
  wex config/changeValue -f=${FILEPATH} -k=${variableName} -v="${original}" -s="${separator}"
  # Get value
  changed=$(wex config/getValue -f="${FILEPATH}" -k="${variableName}" -s="${separator}")
  # Check
  _wexTestAssertEqual "${changed}" "${original}"
}
