#!/usr/bin/env bash

_wexTestAssertNotEmpty() {
  local VALUE
  VALUE=${1}

  if [ "${VALUE}" = '' ]; then
    _wexTestResultError 'Value must not be empty'
  else
    _wexTestResultSuccess 'Value is not empty'
  fi
}

_wexTestAssertEqual() {
  local TEST_VARIABLE=${1}
  local EXPECTED_VALUE=${2}
  if [ "${TEST_VARIABLE}" != "${EXPECTED_VALUE}" ]; then
    TEST_HAS_ERROR=true
    _wexTestResultError "Assertions are not equal"
    _wexTestResultLine "Expected : ${EXPECTED_VALUE}"
    _wexTestResultLine "Got : ${TEST_VARIABLE}"
    exit 1
  else
    _wexTestResultSuccess "Assertions are equal"
    _wexTestResultLine "Value : ${EXPECTED_VALUE}"
  fi
}

_wexTestScriptExists() {
  if [ ! -f "${1}" ]; then
    _wexTestResultError "File does not exists : ${1}"
  else
    _wexTestResultSuccess "File exists : ${1}"
  fi
}

_wexTestResultSuccess() {
  printf "${WEX_COLOR_GREEN}      ✓ Success : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultError() {
  TEST_HAS_ERROR=true
  printf "${WEX_COLOR_RED}      x Error : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultUndefined() {
  printf "${WEX_COLOR_LIGHT_BLUE}      ? Response : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultLine() {
  if [ "${1}" != "" ]; then
    printf "${WEX_COLOR_CYAN}        ${1}${WEX_COLOR_RESET}\n"
  fi
}

_wexTestSampleDiff() {
  local TMP_FILE_NAME
  local EXPECT_CHANGES
  local CONTEXT
  local ORIGINAL
  local MODIFIED
  local DIFF
  local HAS_ERROR

  TMP_FILE_NAME=${1}
  EXPECT_CHANGES=${2}
  CONTEXT=${3}
  ORIGINAL=$(<"${WEX_TEST_RUN_DIR_SAMPLES}${TMP_FILE_NAME}")
  MODIFIED=$(<"${WEX_TEST_DIR_TMP}${TMP_FILE_NAME}")
  DIFF=$(diff <(echo "${ORIGINAL}") <(echo "${MODIFIED}"))
  HAS_ERROR=false

  if [ "${EXPECT_CHANGES}" == "false" ] && [ "${DIFF}" != '' ]; then
    HAS_ERROR="Differences"
  fi

  if [ "${EXPECT_CHANGES}" == "true" ] && [ "${DIFF}" == '' ]; then
    HAS_ERROR="Missing differences"
  fi

  if [ "${HAS_ERROR}" != "false" ]; then
    _wexTestResultError "${HAS_ERROR} found for : ${CONTEXT}"
    _wexTestResultLine "In ${TMP_FILE_NAME}"
    _wexTestResultLine "Diff : \"${DIFF}\""
  else
    _wexTestResultSuccess "Diff succeed : ${CONTEXT}"
    _wexTestResultLine "In ${TMP_FILE_NAME}"
  fi
}

_wexTestSampleInit() {
  TMP_FILE_NAME=${1}
  # Create temp dir if missing.
  mkdir -p "${WEX_TEST_DIR_TMP}"
  # Copy sample file.
  cp "${WEX_TEST_RUN_DIR_SAMPLES}${TMP_FILE_NAME}" "${WEX_TEST_DIR_TMP}"
  # Return file name
  echo "${WEX_TEST_DIR_TMP}${TMP_FILE_NAME}"
}

_wexTestClearTempDir() {
  # Empty temp directory
  rm -rf "${WEX_TEST_DIR_TMP}"
  mkdir -p "${WEX_TEST_DIR_TMP}"
}

wexTest() {
  if [ -z "${1}" ]; then
    _wexTestAppArgs app::app app_dir
    _wexTestRArgsSection "${@}"
  fi

  _wexTestRunTests "${@}"
  _wexTestTrace "${@}"
}

_wexTestRArgsSection() {
  . "${WEX_DIR_ROOT}includes/globals.sh"

  # Add executed methods to global trace file
  echo "" >"${WEX_FILE_TRACE_TESTS}"

  local LOCATIONS
  local SCRIPTS
  local SCRIPT_PATH

  LOCATIONS=$(_wexFindScriptsLocations)
  for LOCATION in ${LOCATIONS[@]}; do
    local ADDON=$(_wexGetAddonFromPath $LOCATION)
    SCRIPTS=($(wex-exec scripts/list -d="${LOCATION}"))

    for SCRIPT in ${SCRIPTS[@]}; do
      SCRIPT_PATH=$(_wexFindScriptFile ${ADDON}::${SCRIPT})

      if [ -f "${SCRIPT_PATH}" ]; then
        if [ "$(_wexLoadArguments "${SCRIPT_PATH}")" = true ]; then
          _wexTestResultSuccess "Args section found in ${SCRIPT_PATH}"
        else
          _wexTestResultError "Args section with description are required for core and addons, not found in : ${SCRIPT_PATH}"
          exit 1
        fi
      fi
    done
  done
}

# Returns the list of all app scripts in the addons directory
_wexTestGetAllAppScriptsFromAddonAndGroup() {
  local ADDON_GROUP="$1"
  local ADDON="${ADDON_GROUP%%::*}"
  local GROUP="${ADDON_GROUP#*::}"
  local ADDON_APP_DIR="${WEX_DIR_ADDONS}${ADDON}/bash/${GROUP}/"
  local ALL_APP_SCRIPTS=()

  if [ -d "${ADDON_APP_DIR}" ]; then
    ALL_APP_SCRIPTS=($(find "${ADDON_APP_DIR}" -type f -name "*.sh" | sort))
  fi

  echo "${ALL_APP_SCRIPTS[@]}"
}

# Checks if all app scripts contain the required function
_wexTestAppArgs() {
  local ALL_APP_SCRIPTS=($(_wexTestGetAllAppScriptsFromAddonAndGroup "${1}"))
  local SEARCH_ARG=${2}

  for SCRIPT in "${ALL_APP_SCRIPTS[@]}"; do
    if [ "$(_wexTestAppArgsFile "${SEARCH_ARG}" "${SCRIPT}")" = "true" ]; then
      _wexTestResultSuccess "Argument '${SEARCH_ARG}' is present in ${SCRIPT}."
    else
      _wexTestResultError "Argument '${SEARCH_ARG}' is missing in ${SCRIPT}."
      exit 1
    fi
  done
}

_wexLoadArguments() {
  local SCRIPT=${1}
  local SCRIPT_CALL_NAME
  local SCRIPT_ARGS

  SCRIPT_CALL_NAME=$(_wexGetCommandNameFromPath "${SCRIPT}")
  SCRIPT_ARGS=$(_wexMethodNameArgs "${SCRIPT_CALL_NAME}")
  _ARGUMENTS=()

  . "${SCRIPT}"

  if [[ $(type -t "${SCRIPT_ARGS}") = "function" ]]; then
    ${SCRIPT_ARGS}

    echo true
    return
  fi

  echo false
}

_wexTestAppArgsFile() {
  local SEARCH_ARG=${1}
  local SCRIPT=${2}
  local SCRIPT_CALL_NAME
  local SCRIPT_ARGS
  local _ARGUMENTS

  SCRIPT_CALL_NAME=$(_wexGetCommandNameFromPath "${SCRIPT}")
  SCRIPT_ARGS=$(_wexMethodNameArgs "${SCRIPT_CALL_NAME}")
  _ARGUMENTS=()

  . "${SCRIPT}"

  if [[ $(type -t "${SCRIPT_ARGS}") = "function" ]]; then
    ${SCRIPT_ARGS}

    for ARGUMENT in "${_ARGUMENTS[@]}"; do
      if [[ "$ARGUMENT" =~ (^|[[:space:]])${SEARCH_ARG}($|[[:space:]]) ]]; then
        echo true
        return
      fi
    done
  fi

  echo false
}

_wexTestRunTests() {
  export WEX_TRACE_CALLS=true

  # List only directories.
  local SCRIPTS
  local SCRIPT_FILEPATH
  local TEST_RUN_SCRIPT="${1}"
  local WEX_TEST_DIRS=("$(_wexFindScriptsLocations)")
  local TEST_ACTION=${2:-run}
  local PATH_DIR_ROOT
  local PATH_DIR_TESTS_BASH

  if [ "${TEST_ACTION}" == "run" ]; then
    for PATH_DIR_BASH in ${WEX_TEST_DIRS[@]}; do
      PATH_DIR_ROOT=$(dirname "${PATH_DIR_BASH}")
      PATH_DIR_TESTS_BASH="${PATH_DIR_ROOT}/tests/bash/"

      # Ignore missing bash dirs
      if [ -d "${PATH_DIR_TESTS_BASH}" ]; then

        local PATH_TEST_INIT="${PATH_DIR_TESTS_BASH}init.sh"
        if [ -f "${PATH_TEST_INIT}" ]; then
          _wexLog "Initializing... ${PATH_TEST_INIT}"

          . "${PATH_TEST_INIT}"
        fi

        if [ "${TEST_RUN_SCRIPT}" == "" ]; then
          _wexLog "Testing dir ... ${PATH_DIR_TESTS_BASH}"

          SCRIPTS=($(wex-exec scripts/list -d="${PATH_DIR_TESTS_BASH}"))

          for SCRIPT_NAME in ${SCRIPTS[@]}; do
            _wexTestScript "${SCRIPT_NAME}"
          done
        fi
      fi
    done

    if [ "${TEST_RUN_SCRIPT}" != "" ]; then
      _wexTestScript "${TEST_RUN_SCRIPT}"
      return
    fi
  elif [ "${TEST_ACTION}" == "create" ] && [ "${TEST_RUN_SCRIPT}" != "" ]; then
    local TEST_FILE
    local METHOD_NAME
    TEST_FILE="$(_wexTestGetFile "${TEST_RUN_SCRIPT}")"
    METHOD_NAME="$(_wexMethodName "${TEST_RUN_SCRIPT}")Test"

    cat <<EOF >"${TEST_FILE}"
#!/usr/bin/env bash

${METHOD_NAME}() {
  # TODO : Your test body.
  _wexTestAssertEqual true false
}

EOF
    _wexLog "Created ${TEST_FILE}"
    return
  fi
}

_wexTestTrace() {
  local TRACED_COMMANDS
  local MISSING_COUNT=0

  TRACED_COMMANDS=$(sort "${WEX_FILE_TRACE_TESTS}" | uniq)

  for SCRIPT_PATH in $(cat "${WEX_FILE_ALL_SCRIPTS_PATHS}"); do
    local FOUND=false

    for TRACED_COMMAND in ${TRACED_COMMANDS[@]}; do
      if [ "${FOUND}" = "false" ] && [[ $(echo "${SCRIPT_PATH}" | grep "${TRACED_COMMAND}#") != "" ]]; then
        FOUND=true
      fi
    done

    if [ ${FOUND} == false ]; then
      _wexTestResultError "No test ran for command : $(echo "${SCRIPT_PATH}" | cut -d '#' -f 1)"
      MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
  done

  if [ ${MISSING_COUNT} != 0 ]; then
    _wexTestResultError "Missing tests : ${MISSING_COUNT}"
  fi
}

_wexTestGetFile() {
  local SCRIPT_NAME=${1}
  local SCRIPT_FILEPATH=$(_wexFindScriptFile "${SCRIPT_NAME}")
  local PATH_DIR_TESTS_BASH=$(realpath $(dirname "${SCRIPT_FILEPATH}")/../../)/tests/bash/

  echo "${PATH_DIR_TESTS_BASH}${SCRIPT_NAME}.sh"
}

_wexTestScript() {
  local SCRIPT_NAME=${1}
  local SCRIPT_FILEPATH
  local PATH_DIR_TESTS_BASH
  SCRIPT_FILEPATH=$(_wexFindScriptFile "${SCRIPT_NAME}")
  PATH_DIR_TESTS_BASH=$(realpath $(dirname ${SCRIPT_FILEPATH})/../../)/tests/bash/
  TEST_FILE="$(_wexTestGetFile "${SCRIPT_NAME}")"
  METHOD_NAME="$(_wexMethodName "${SCRIPT_NAME}")Test"

  local WEX_TEST_RUN_DIR_SAMPLES=${PATH_DIR_TESTS_BASH}"_samples/"
  local TEST_HAS_ERROR

  _wexLog "Script ${SCRIPT_NAME} __________________________"
  _wexLog "Script file ${SCRIPT_FILEPATH}"
  _wexLog "Test file ${TEST_FILE}"

  # Import test methods
  . "${TEST_FILE}"

  local TEST_HAS_ERROR=false

  if [ "$(type -t "${METHOD_NAME}" 2>/dev/null)" = "function" ]; then
    "${METHOD_NAME}" ${_TEST_ARGUMENTS[@]}
  else
    _wexError "Test file exists but missing method : ${METHOD_NAME}"
    exit 1
  fi

  if [ "${TEST_HAS_ERROR}" = "false" ]; then
    _wexTestResultSuccess "Test complete"
  else
    _wexTestResultError "Test failed"
    exit 1
  fi
}

_wexTestFileExists() {
  local FILEPATH="$1"

  if [ -f "$FILEPATH" ]; then
    _wexTestResultSuccess "File $FILEPATH exists."
  else
    _wexTestResultError "File $FILEPATH does not exist."
  fi
}

export -f _wexTestAssertEqual
export -f _wexTestAssertNotEmpty
export -f _wexTestClearTempDir
export -f _wexTestFileExists
export -f _wexTestGetFile
export -f _wexTestSampleDiff
export -f _wexTestResultError
export -f _wexTestScriptExists
export -f _wexTestSampleInit
export -f _wexTestResultLine
export -f _wexTestResultSuccess
export -f _wexTestResultUndefined
export -f _wexTestScript
