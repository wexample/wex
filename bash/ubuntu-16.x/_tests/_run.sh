#!/usr/bin/env bash

# Store current dir.
_TEST_RUN_DIR_CURRENT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
_TEST_RUN_DIR_SAMPLES=${_TEST_RUN_DIR_CURRENT}samples/
_TEST_RUN_SCRIPT=${1}

# Fix same directory location for all tests.
cd ${_TEST_RUN_DIR_CURRENT}

# Avoid prompting user.
WEX_NON_INTERACTIVE=true

wexampleTestError() {
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

for DIR in "${_TEST_RUN_DIR_CURRENT}"*
do
  DIR_NAME=$(basename "${DIR}")
  FIRST_LETTER="$(echo ${DIR_NAME} | head -c 1)"

  # Exclude folders with _ prefix.
  if [[ "${FIRST_LETTER}" != "_" ]]; then

    # Iterate group folder
    for FILE in "${_TEST_RUN_DIR_CURRENT}${DIR_NAME}/"*
    do
      TEST_FILE_NAME=$(basename "${FILE}")
      SCRIPT_CALL_NAME=${DIR_NAME}"/${TEST_FILE_NAME%.*}"
      FIRST_LETTER="$(echo ${FILE} | head -c 1)"

      # Exclude files with _ prefix.
      # Allow to specify single script name to test.
      if [[ "${FIRST_LETTER}" != "_" && ("${_TEST_RUN_SCRIPT}" == "" || ${_TEST_RUN_SCRIPT} == ${SCRIPT_CALL_NAME}) ]]; then
        METHOD_NAME=$(wexampleMethodName ${SCRIPT_CALL_NAME})

        # Build script file path.
        _TEST_SCRIPT_FILE="${_TEST_RUN_DIR_CURRENT}${SCRIPT_CALL_NAME}.sh"

        # Clear defined function
        _TEST_ARGUMENTS=false

        echo "Testing ${SCRIPT_CALL_NAME}"

        # Import test methods
        . "${_TEST_SCRIPT_FILE}"

        echo "Execute wex ${SCRIPT_CALL_NAME} ${_TEST_ARGUMENTS[@]}"
        if [[ $(type -t "${METHOD_NAME}Test" 2>/dev/null) == function ]]; then
          echo "  > Custom ${METHOD_NAME}Test method"
          testResult=$(${METHOD_NAME}Test ${METHOD_NAME}Test ${_TEST_ARGUMENTS[@]})
        else
          echo "  > Auto test method : wex ${SCRIPT_CALL_NAME} --nonInteractive ${_TEST_ARGUMENTS[@]}"
          wex ${SCRIPT_CALL_NAME} --nonInteractive ${_TEST_ARGUMENTS[@]}
          # Run script and store result.
          testResult=$(wex ${SCRIPT_CALL_NAME} --nonInteractive ${_TEST_ARGUMENTS[@]})
        fi;

        # Print result for info.
        echo "  > Test response : ${testResult}"

        if [[ $(type -t "${METHOD_NAME}Verify" 2>/dev/null) == function ]]; then
          ${METHOD_NAME}Verify "${testResult}"
        fi;
      fi;
    done
  fi;
done
