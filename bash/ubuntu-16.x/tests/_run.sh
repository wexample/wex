#!/usr/bin/env bash

# Store current dir.
_TEST_RUN_DIR_CURRENT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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

# Import wexample.sh
. "${_TEST_RUN_DIR_CURRENT}/../wexample.sh" ${1}

for testFile in "${_TEST_RUN_DIR_CURRENT}"/*
do
  fileName=$(basename "${testFile}")
  fileName="${fileName%.*}"
  firstLetter="$(echo $fileName | head -c 1)"
  # Exclude files with _ prefix.
  if [ "${firstLetter}" != "_" ]; then
    # Import test methods
    echo "ok";
    . "${_TEST_RUN_DIR_CURRENT}/${fileName}.sh"

    # TODO predefined arguments into test file.

    # Run script and store result.
    testResult=$(wexampleRun -s=${fileName})

    verify "${testResult}"
  fi;
done

