#!/usr/bin/env bash

_wexTestAssertEqual() {
  local TEST_VARIABLE=${1}
  local EXPECTED_VALUE=${2}
  if [ "${TEST_VARIABLE}" != "${EXPECTED_VALUE}" ]; then
    WEX_TEST_HAS_ERROR=true
    _wexTestResultError "Assertions are not equal"
    _wexTestResultLine "Expected : ${EXPECTED_VALUE}"
    _wexTestResultLine "Got : ${TEST_VARIABLE}"
    exit 1
  else
    _wexTestResultSuccess "Assertions are equal"
    _wexTestResultLine "Value : ${EXPECTED_VALUE}"
  fi;
}

_wexTestResultSuccess() {
  printf ${WEX_COLOR_GREEN}"      ✓ Success : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultError() {
  WEX_TEST_HAS_ERROR=true
  printf ${WEX_COLOR_RED}"      x Error : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultUndefined() {
  printf ${WEX_COLOR_LIGHT_BLUE}"      ? Response : ${1}${WEX_COLOR_RESET}\n"
  _wexTestResultLine ${2}
}

_wexTestResultLine() {
  if [ "${1}" != "" ];then
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
  ORIGINAL=$(< "${WEX_TEST_RUN_DIR_SAMPLES}${TMP_FILE_NAME}")
  MODIFIED=$(< "${WEX_TEST_DIR_TMP}${TMP_FILE_NAME}")
  DIFF=$(diff <(echo "${ORIGINAL}") <(echo "${MODIFIED}"))
  HAS_ERROR=false

  if [ "${EXPECT_CHANGES}" == "false" ] && [ "${DIFF}" != '' ]; then
    HAS_ERROR="Differences"
  fi

  if [ "${EXPECT_CHANGES}" == "true" ] && [ "${DIFF}" == '' ]; then
    HAS_ERROR="Missing differences"
  fi

  if [ "${HAS_ERROR}" != "false" ];then
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
  # List only directories.
  local WEX_TEST_NAMESPACES=($(ls -d ${WEX_DIR_BASH}*/))
  local WEX_TEST_RUN_SCRIPT=${1}

  . "${WEX_DIR_BASH}globals.sh"

  for DIR in ${WEX_TEST_NAMESPACES[@]}
  do
    local NAMESPACE=$(basename ${DIR})
    local SPLIT=($(echo ${WEX_TEST_RUN_SCRIPT}| tr ":" "\n"))
    # If no specified script
    # Or no specified namespace
    # Or a namespace is specified and the same as current
    if [[ -z "${WEX_TEST_RUN_SCRIPT:+x}" ]] || [[ -z "${SPLIT[1]:+x}" ]] || [[ ${SPLIT[0]} == ${NAMESPACE} ]];then
      local WEX_TEST_RUN_DIR_CURRENT=${WEX_DIR_ROOT}"tests/bash/"${NAMESPACE}"/"

      # Dir exists.
      if [[ -d ${WEX_TEST_RUN_DIR_CURRENT} ]];then
        local WEX_TEST_RUN_DIR_SAMPLES=${WEX_TEST_RUN_DIR_CURRENT}"_samples/"
        # Get all folder.
        local WEX_TESTS_NAMESPACE_FOLDERS=($(ls ${WEX_TEST_RUN_DIR_CURRENT}))
        local WEX_TEST_DIR_NAME

        for WEX_TEST_DIR_NAME in ${WEX_TESTS_NAMESPACE_FOLDERS[@]}
        do
          local WEX_TEST_FIRST_LETTER="$(echo ${WEX_TEST_DIR_NAME} | head -c 1)"

          # Exclude folders with _ prefix.
          if [ "${WEX_TEST_FIRST_LETTER}" != "_" ]; then
            local WEX_TESTS_NAMESPACE_FOLDERS_FILES=($(ls ${WEX_TEST_RUN_DIR_CURRENT}${WEX_TEST_DIR_NAME}))
            # Iterate group folder
            for WEX_TEST_FILE in ${WEX_TESTS_NAMESPACE_FOLDERS_FILES[@]}
            do
              local WEX_TEST_FILE_NAME=$(basename "${WEX_TEST_FILE}")
              local WEX_TEST_SCRIPT_CALL_NAME=${WEX_TEST_DIR_NAME}"/${WEX_TEST_FILE_NAME%.*}"
              local WEX_TEST_FIRST_LETTER="$(echo "${WEX_TEST_FILE}" | head -c 1)"

              # Exclude files with _ prefix.
              # Allow to specify single script name to test.
              if [[ "${WEX_TEST_FIRST_LETTER}" != "_" && ("${WEX_TEST_RUN_SCRIPT}" == "" || ${WEX_TEST_RUN_SCRIPT} == ${WEX_TEST_SCRIPT_CALL_NAME} || ${WEX_TEST_RUN_SCRIPT} == ${NAMESPACE}::${WEX_TEST_SCRIPT_CALL_NAME}) ]]; then
                local WEX_TEST_METHOD_NAME=$(_wexMethodName "${WEX_TEST_SCRIPT_CALL_NAME}")

                # Build script file path.
                local _TEST_SCRIPT_FILE="${WEX_TEST_RUN_DIR_CURRENT}${WEX_TEST_SCRIPT_CALL_NAME}.sh"
                # Clear defined function
                local _TEST_ARGUMENTS=

                # Import test methods
                . "${_TEST_SCRIPT_FILE}"

                _wexMessage "test ${NAMESPACE}::${WEX_TEST_SCRIPT_CALL_NAME}" "${NAMESPACE}/${WEX_TEST_SCRIPT_CALL_NAME}.sh"

                # Go to test dir.
                cd "${WEX_TEST_RUN_DIR_CURRENT}"

                WEX_TEST_HAS_ERROR=false
                if [ "$(type -t "${WEX_TEST_METHOD_NAME}Test" 2>/dev/null)" = "function" ]; then
                    # Do not encapsulate result
                    "${WEX_TEST_METHOD_NAME}Test" ${_TEST_ARGUMENTS[@]}
                fi

                if [ "${WEX_TEST_HAS_ERROR}" = "false" ]; then
                  _wexTestResultSuccess "Test complete"
                else
                  _wexTestResultError "Test failed"
                fi
              fi
            done
          fi
        done
      fi
    fi
  done
}

wexTest "${@}"