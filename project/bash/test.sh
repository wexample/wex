#!/usr/bin/env bash

WEX_TEST_DIR_TMP="${WEX_DIR_TMP}test/"

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

_wexTestFileExists() {
  if [ ! -f "${1}" ];then
    _wexTestResultError "File does not exists : ${1}"
  else
    _wexTestResultSuccess "File exists : ${1}"
  fi
}

_wexTestResultSuccess() {
  printf ${WEX_COLOR_GREEN}"      ✓ Success : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultError() {
  TEST_HAS_ERROR=true
  printf ${WEX_COLOR_RED}"      x Error : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultUndefined() {
  printf ${WEX_COLOR_LIGHT_BLUE}"      ? Response : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultLine() {
  if [ "${1}" != "" ]; then
    printf ${WEX_COLOR_CYAN}"        ${1}${WEX_COLOR_RESET}\n"
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

wexTest() {
  . "${WEX_DIR_ROOT}includes/globals.sh"

  # List only directories.
  local METHOD_NAME
  local SCRIPTS
  local SCRIPT_FILEPATH
  local TEST_HAS_ERROR
  local TEST_RUN_SCRIPT="${1}"
  local TEST_FILE
  local WEX_TEST_DIRS=("$(_wexFindScriptsLocations)")

  for PATH_DIR_BASH in ${WEX_TEST_DIRS[@]}; do
    _wexLog "Testing ... ${WEX_TEST_RUN_DIR_CURRENT}"

    local PATH_DIR_ROOT=$(realpath "${PATH_DIR_BASH}../")
    local PATH_DIR_TESTS_BASH="${PATH_DIR_ROOT}/tests/bash/"
    local WEX_TEST_RUN_DIR_SAMPLES=${PATH_DIR_TESTS_BASH}"_samples/"

    SCRIPTS=$(wex scripts/list -d="${PATH_DIR_BASH}")

    for SCRIPT_NAME in ${SCRIPTS[@]}; do
      SCRIPT_FILEPATH=$(_wexFindScriptFile "${SCRIPT_NAME}")

      # Exclude files with _ prefix.
      # Allow to specify single script name to test.
      if [ "${TEST_RUN_SCRIPT}" = "" ] || [ "${TEST_RUN_SCRIPT}" = "${SCRIPT_NAME}" ]; then
        # Build script file path.
        TEST_FILE="${PATH_DIR_TESTS_BASH}${SCRIPT_NAME}.sh"

        if [ ! -f "${TEST_FILE}" ]; then
          _wexError "Missing test for script ${SCRIPT_NAME}, expecting : ${TEST_FILE}"
          return
        fi

        # Import test methods
        . "${TEST_FILE}"

        METHOD_NAME="$(_wexMethodName "${SCRIPT_NAME}")Test"
        TEST_HAS_ERROR=false

        _wexMessage "testing ${SCRIPT_NAME}"
        _wexLog "Script file : ${SCRIPT_FILEPATH}"
        _wexLog "Test file   : ${TEST_FILE}"
        _wexLog "Test method : ${METHOD_NAME}"

        if [ "$(type -t "${METHOD_NAME}" 2>/dev/null)" = "function" ]; then

          "${METHOD_NAME}" ${_TEST_ARGUMENTS[@]}
        else
          _wexError "Test file exists but missing method : ${METHOD_NAME}"
          return
        fi

        if [ "${TEST_HAS_ERROR}" = "false" ]; then
          _wexTestResultSuccess "Test complete"
        else
          _wexTestResultError "Test failed"
        fi
      fi
    done
  done
}

wexTest "${@}"
