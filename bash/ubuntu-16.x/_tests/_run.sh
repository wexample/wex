#!/usr/bin/env bash

# Store current dir.
_TEST_RUN_DIR_CURRENT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
_TEST_RUN_DIR_SAMPLES=${_TEST_RUN_DIR_CURRENT}_samples/
_TEST_RUN_SCRIPT=${1}
WEX_TEST_HAS_ERROR=false

# Fix same directory location for all tests.
cd ${_TEST_RUN_DIR_CURRENT}

# Avoid prompting user.
WEX_NON_INTERACTIVE=true

wexampleTestError() {
  WEX_TEST_HAS_ERROR=true
  RED='\033[1;31m'
  NC='\033[0m'
  echo -e "${RED}"
  echo "Test error : "${1}
  echo -e "${NC}"
  exit 1;
}

wexampleTestAssertEqual() {
  TEST_VARIABLE=${1}
  EXPECTED_VALUE=${2}
  if [ "${TEST_VARIABLE}" != "${EXPECTED_VALUE}" ]; then
    WEX_TEST_HAS_ERROR=true
    RED='\033[1;31m'
    NC='\033[0m'
    echo -e "${RED}"
    echo "Assertion are not equal";
    echo "  - Got : ${TEST_VARIABLE}";
    echo "  - Expected : ${EXPECTED_VALUE}";
    echo -e "${NC}"
    exit 1;
  fi;
}

wexampleArrayJoin() {
  local d=$1;
  shift;
  echo -n "$1";
  shift;
  printf "%s" "${@/#/$d}";
}

# Import wexample.sh
. "${_TEST_RUN_DIR_CURRENT}../wexample/wexample.sh" false

# If there is no specified test
if [ "${_TEST_RUN_SCRIPT}" == '' ]; then
  # Revert all samples
  git checkout HEAD -- ${_TEST_RUN_DIR_SAMPLES}*
fi;

for WEX_TEST_DIR in "${_TEST_RUN_DIR_CURRENT}"*
do
  WEX_TEST_DIR_NAME=$(basename "${WEX_TEST_DIR}")
  WEX_TEST_FIRST_LETTER="$(echo ${WEX_TEST_DIR_NAME} | head -c 1)"

  # Exclude folders with _ prefix.
  if [[ "${WEX_TEST_FIRST_LETTER}" != "_" ]]; then

    # Iterate group folder
    for WEX_TEST_FILE in "${_TEST_RUN_DIR_CURRENT}${WEX_TEST_DIR_NAME}/"*
    do
      WEX_TEST_FILE_NAME=$(basename "${WEX_TEST_FILE}")
      WEX_TEST_SCRIPT_CALL_NAME=${WEX_TEST_DIR_NAME}"/${WEX_TEST_FILE_NAME%.*}"
      WEX_TEST_FIRST_LETTER="$(echo ${WEX_TEST_FILE} | head -c 1)"

      # Exclude files with _ prefix.
      # Allow to specify single script name to test.
      if [[ "${WEX_TEST_FIRST_LETTER}" != "_" && ("${_TEST_RUN_SCRIPT}" == "" || ${_TEST_RUN_SCRIPT} == ${WEX_TEST_SCRIPT_CALL_NAME}) ]]; then
        WEX_TEST_METHOD_NAME=$(wexampleMethodName ${WEX_TEST_SCRIPT_CALL_NAME})

        # Build script file path.
        _TEST_SCRIPT_FILE="${_TEST_RUN_DIR_CURRENT}${WEX_TEST_SCRIPT_CALL_NAME}.sh"

        # Clear defined function
        _TEST_ARGUMENTS=

        echo "Testing ${WEX_TEST_SCRIPT_CALL_NAME}"

        # Import test methods
        . "${_TEST_SCRIPT_FILE}"

        echo "Execute wex ${WEX_TEST_SCRIPT_CALL_NAME} ${_TEST_ARGUMENTS[@]}"
        if [[ $(type -t "${WEX_TEST_METHOD_NAME}Test" 2>/dev/null) == function ]]; then
          echo "  > Custom ${WEX_TEST_METHOD_NAME}Test method"
          testResult=$(${WEX_TEST_METHOD_NAME}Test ${WEX_TEST_METHOD_NAME}Test ${_TEST_ARGUMENTS[@]})
        else
          echo "  > Auto test method : wex ${WEX_TEST_SCRIPT_CALL_NAME} --nonInteractive ${_TEST_ARGUMENTS[@]}"
          # Run script and store result.
          testResult=$(wex ${WEX_TEST_SCRIPT_CALL_NAME} --nonInteractive ${_TEST_ARGUMENTS[@]})
        fi;

        if [[ "${testResult}" == "" && ${WEX_TEST_HAS_ERROR} == false ]]; then
          GREEN='\033[1;32m'
          NC='\033[0m'
          echo -e "${GREEN}"
          echo "  > Test success"
          echo -e "${NC}"
        else
          # Print result for info.
          echo "  > Test response : ${testResult}"
        fi;

        if [[ $(type -t "${WEX_TEST_METHOD_NAME}Verify" 2>/dev/null) == function ]]; then
          ${WEX_TEST_METHOD_NAME}Verify "${testResult}"
        fi;
      fi;
    done
  fi;
done
