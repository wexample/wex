#!/usr/bin/env bash

test() {
  # Get the last line
  fileGetLastFilledLine=$(wexample fileGetLastFilledLine "${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt")
  # Compare
  wexampleTestAssertEqual "${fileGetLastFilledLine}" "[LAST LINE]"
}
