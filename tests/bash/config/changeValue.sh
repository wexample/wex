#!/usr/bin/env bash

configChangeValueTest() {
  local RESULT
  local FILEPATH
  FILEPATH=$(_wexTestSampleInit configSample)

  # No separator
  RESULT=$(wex default::config/getValue -f="${FILEPATH}" -k="ConfigTestOption")
  _wexTestAssertEqual "${RESULT}" "two"

  # Space separator
  configChangeValueTestItem "${FILEPATH}" "ConfigTestOption" " "

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  # Strict equal separator
  configChangeValueTestItem "${FILEPATH}" "ConfigTestOptionEqual" "="

  # Revert file.
  FILEPATH=$(_wexTestSampleInit configSample)

  configChangeValueTestItem "${FILEPATH}" "ChallengeResponseAuthentication" " "

  FILEPATH=$(_wexTestSampleInit sshd_config)
  configChangeValueTestItem "${FILEPATH}" Port " "
}

configChangeValueTestItem() {
  local FILEPATH="${1}"
  local NAME="${2}"
  local SEPARATOR="${3}"
  local EXPECTED="tested"
  local ORIGINAL

  # Backup
  ORIGINAL=$(wex default::config/getValue -f="${FILEPATH}" -k="${NAME}" -s="${SEPARATOR}")

  # Set value.
  wex default::config/changeValue -f="${FILEPATH}" -k="${NAME}" -v="${EXPECTED}" -s="${SEPARATOR}"
  configChangeValueTestItemCheck "${EXPECTED}"

  # Revert
  wex default::config/changeValue -f="${FILEPATH}" -k="${NAME}" -v="${ORIGINAL}" -s="${SEPARATOR}"
  configChangeValueTestItemCheck "${ORIGINAL}"

  # Remove
  wex default::config/removeKey -f="${FILEPATH}" -k="${NAME}" -s="${SEPARATOR}"
  configChangeValueTestItemCheck ""

  # Reset
  wex default::config/setValue -f="${FILEPATH}" -k="${NAME}" -v="${ORIGINAL}" -s="${SEPARATOR}"
  configChangeValueTestItemCheck "${ORIGINAL}"
}

configChangeValueTestItemCheck() {
  # Check
  _wexTestAssertEqual "$(wex default::config/getValue -f="${FILEPATH}" -k="${NAME}" -s="${SEPARATOR}")" "${1}"
}
