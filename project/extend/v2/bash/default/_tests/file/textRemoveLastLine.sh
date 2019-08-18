#!/usr/bin/env bash

. "${_TEST_RUN_DIR_CURRENT}file/textAppend.sh"

fileTextRemoveLastLineTest() {
  fileTextAppendTest "$@"
}
