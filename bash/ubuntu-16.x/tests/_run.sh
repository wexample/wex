#!/usr/bin/env bash

# Store current dir.
_TEST_RUN_DIR_CURRENT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_TEST_RUN_SCRIPT=${1}

wexampleTestAssertEqual() {
  TEST_VARIABLE=${1}
  EXPECTED_VALUE=${2}
  if [ "${TEST_VARIABLE}" != "${EXPECTED_VALUE}" ]; then
    echo "Assertion are not equal";
    echo "  - Expected : ${EXPECTED_VALUE}";
    echo "  - Got : ${TEST_VARIABLE}";
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
. "${_TEST_RUN_DIR_CURRENT}/../wexample.sh" ${1}

for testFile in "${_TEST_RUN_DIR_CURRENT}"/*
do
  fileName=$(basename "${testFile}")
  fileName="${fileName%.*}"
  firstLetter="$(echo $fileName | head -c 1)"

  # Exclude files with _ prefix.
  # Allow to specify single script name to test.
  if [[ "${firstLetter}" != "_" && ("${_TEST_RUN_SCRIPT}" == "" || ${_TEST_RUN_SCRIPT} == ${fileName}) ]]; then

  # Build script file path.
  _TEST_RUN_FILE="${_TEST_RUN_DIR_CURRENT}/${fileName}.sh"

  # File does not exists.
  if [ -f ${testFile} ]; then
    # Clear defined function
    arguments=false
    verify=false

    # Import test methods
    . "${_TEST_RUN_FILE}"

    # Print returned value for info.
    if [[ $(type -t "arguments" 2>/dev/null) == function ]]; then
      arguments
      argumentsJoined=$(wexampleArrayJoin " " ${arguments[@]})
    else
      argumentsJoined=''
    fi;

    echo "Execute wexampleRun -s=${fileName} -a=\"${argumentsJoined}\""
    # Run script and store result.
    testResult=$(wexampleRun -s=${fileName} -a="${argumentsJoined}")

    # Print result for info.
    echo "              > ${testResult}"

    if [ "${arguments}" != false ]; then
    verify "${testResult}"
    fi;

  else
    echo "Missing test file ${testFile}";
    exit 1;
   fi;
  fi;
done
