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
  fileName="${fileName%.*}"
  firstLetter="$(echo $fileName | head -c 1)"

  # Exclude files with _ prefix.
  # Allow to specify single script name to test.
  if [[ "${firstLetter}" != "_" && ("${_TEST_RUN_SCRIPT}" == "" || ${_TEST_RUN_SCRIPT} == ${fileName}) ]]; then

  # Build script file path.
  _TEST_RUN_FILE="${_TEST_RUN_DIR_CURRENT}${fileName}.sh"

  # File does not exists.
  if [ -f ${testFile} ]; then
    # Clear defined function
    _TEST_ARGUMENTS=false
    test=false
    verify=false

    echo "Testing ${fileName}"

    # Import test methods
    . "${_TEST_RUN_FILE}"

    echo "Execute wexample ${fileName} ${_TEST_ARGUMENTS[@]}"
    if [ "${test}" != false ] ; then
      testResult=$(test ${fileName} ${_TEST_ARGUMENTS[@]})
    else
      # Run script and store result.
      testResult=$(wexample ${fileName} ${_TEST_ARGUMENTS[@]})
    fi;

    # Print result for info.
    echo "              > Test response : ${testResult}"

    if [ "${arguments}" != false ] && [[ $(type -t "verify" 2>/dev/null) == function ]]; then
    verify "${testResult}"
    fi;

  # This is missing and not a directory
  elif [ ! -d ${testFile} ]; then
    echo "Missing test file ${testFile}";
    exit 1;
   fi;
  fi;
done
