#!/usr/bin/env bash

# Store current dir.
_TEST_RUN_DIR_CURRENT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
_TEST_RUN_DIR_SAMPLES=${_TEST_RUN_DIR_CURRENT}samples/
_TEST_RUN_SCRIPT=${1}

wexampleTestAssertEqual() {
  TEST_VARIABLE=${1}
  EXPECTED_VALUE=${2}
  if [ "${TEST_VARIABLE}" != "${EXPECTED_VALUE}" ]; then
    echo "Assertion are not equal";
    echo "  - Expected : ${EXPECTED_VALUE}";
    echo "  - Got : ${TEST_VARIABLE}";
    exit 2;
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
. "${_TEST_RUN_DIR_CURRENT}../wexample.sh" false

for testFile in "${_TEST_RUN_DIR_CURRENT}"*
do
  fileName=$(basename "${testFile}")
  functionName="${fileName%.*}"
  firstLetter="$(echo $functionName | head -c 1)"

  # Exclude files with _ prefix.
  # Allow to specify single script name to test.
  if [[ "${firstLetter}" != "_" && ("${_TEST_RUN_SCRIPT}" == "" || ${_TEST_RUN_SCRIPT} == ${functionName}) ]]; then

  # Build script file path.
  _TEST_RUN_FILE="${_TEST_RUN_DIR_CURRENT}${functionName}.sh"

  # File does not exists.
  if [ -f ${testFile} ]; then
    # Clear defined function
    _TEST_ARGUMENTS=false
    verify=false

    echo "Testing ${functionName}"

    # Import test methods
    . "${_TEST_RUN_FILE}"

    echo "Execute wexample ${functionName} ${_TEST_ARGUMENTS[@]}"
    if [[ $(type -t "${functionName}Test" 2>/dev/null) == function ]]; then
      echo "  > custom ${functionName}Test method"
      testResult=$(${functionName}Test ${functionName}Test ${_TEST_ARGUMENTS[@]})
    else
      echo "  > auto test method"
      # Run script and store result.
      testResult=$(wexample ${functionName} ${_TEST_ARGUMENTS[@]})
    fi;

    # Print result for info.
    echo "  > Test response : ${testResult}"

    if [ "${arguments}" != false ] && [[ $(type -t "${functionName}Verify" 2>/dev/null) == function ]]; then
      ${functionName}Verify "${testResult}"
    fi;

  # This is missing and not a directory
  elif [ ! -d ${testFile} ]; then
    echo "  x Missing test file ${testFile}";
    exit 1;
   fi;
  fi;
done
