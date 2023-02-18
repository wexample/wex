#!/usr/bin/env bash

WEX_TEST_DIR_TMP="${WEX_DIR_TMP}test/"
WEX_TRACE_CALLS=true

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
  . "${WEX_DIR_ROOT}includes/globals.sh"

  WEX_TRACE_CALLS=true

  # List only directories.
  local SCRIPTS
  local SCRIPT_FILEPATH
  local TEST_RUN_SCRIPT="${1}"
  local WEX_TEST_DIRS=("$(_wexFindScriptsLocations)")
  local TEST_ACTION=${2:-run}
  WEX_FILE_TRACE_TESTS="${WEX_FILE_TRACE}.tests"

  if [ "${TEST_ACTION}" == "run" ]; then
    for PATH_DIR_BASH in ${WEX_TEST_DIRS[@]}; do
      local PATH_DIR_ROOT=$(dirname "${PATH_DIR_BASH}")
      local PATH_DIR_TESTS_BASH="${PATH_DIR_ROOT}/tests/bash/"

      # Ignore missing bash dirs
      if [ -d "${PATH_DIR_TESTS_BASH}" ]; then

        local PATH_TEST_INIT="${PATH_DIR_TESTS_BASH}init.sh"
        if [ -f "${PATH_TEST_INIT}" ]; then
          _wexLog "Initializing..."

          . "${PATH_TEST_INIT}"
        fi

        _wexLog "Testing dir ... ${PATH_DIR_TESTS_BASH}"

        if [ "${TEST_RUN_SCRIPT}" == "" ]; then
          SCRIPTS=($(wex scripts/list -d="${PATH_DIR_TESTS_BASH}"))

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
  fi

  local TRACED_COMMANDS=$(sort "${WEX_FILE_TRACE_TESTS}" | uniq)
  local MISSING_COUNT=0

  for SCRIPT_PATH in $(cat "${WEX_FILE_ALL_SCRIPTS_PATHS}"); do
    local FOUND=false

    for TRACED_COMMAND in ${TRACED_COMMANDS[@]}; do
      if [ "${FOUND}" = "false" ] && [[ $(echo "${SCRIPT_PATH}" | grep "${TRACED_COMMAND}#") != "" ]]; then
        FOUND=true
      fi
    done

    if [ ${FOUND} == false ]; then
      _wexTestResultError "No test ran for command : $(echo "${SCRIPT_PATH}" | cut -d '#' -f 1)"
      MISSING_COUNT=$((MISSING_COUNT+1))
    fi
  done

  if [ ${MISSING_COUNT} != 0 ]; then
    _wexTestResultError "Missing tests : ${MISSING_COUNT}"
  fi
}

_wexTestScript() {
  local SCRIPT_NAME=${1}
  local SCRIPT_FILEPATH
  local PATH_DIR_TESTS_BASH
  SCRIPT_FILEPATH=$(_wexFindScriptFile "${SCRIPT_NAME}")
  PATH_DIR_TESTS_BASH=$(realpath $(dirname ${SCRIPT_FILEPATH})/../../)/tests/bash/
  TEST_FILE="${PATH_DIR_TESTS_BASH}${SCRIPT_NAME}.sh"
  METHOD_NAME="$(_wexMethodName "${SCRIPT_NAME}")Test"

  local WEX_TEST_RUN_DIR_SAMPLES=${PATH_DIR_TESTS_BASH}"_samples/"
  local TEST_HAS_ERROR

  _wexLog "Script ${SCRIPT_NAME}"
  _wexLog "Script file ${SCRIPT_FILEPATH}"
  _wexLog "Test file ${TEST_FILE}"

  # Import test methods
  . "${TEST_FILE}"

  local TEST_HAS_ERROR=false

  if [ "$(type -t "${METHOD_NAME}" 2>/dev/null)" = "function" ]; then
    "${METHOD_NAME}" ${_TEST_ARGUMENTS[@]}

    # Add executed methods to global trace file
    cat "${WEX_FILE_TRACE}" >> "${WEX_FILE_TRACE_TESTS}"
  else
    _wexError "Test file exists but missing method : ${METHOD_NAME}"
    exit
  fi

  if [ "${TEST_HAS_ERROR}" = "false" ]; then
    _wexTestResultSuccess "Test complete"
  else
    _wexTestResultError "Test failed"
  fi
}

wexTest "${@}"
