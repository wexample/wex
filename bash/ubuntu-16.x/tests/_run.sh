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
.  "${_TEST_RUN_DIR_CURRENT}/../wexample.sh" ${1}
# Import test methods
. "${_TEST_RUN_DIR_CURRENT}/${1}.sh"

# TODO predefined arguments into test file.

# Run script and store result.
testResult=$(wexampleRun -s=${1})

verify "${testResult}"
