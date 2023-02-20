#!/usr/bin/env bash

fileCreateIfNotExistsTest() {
  local FILEPATH="${WEX_TEST_DIR_TMP}testFile"

  wex-exec file/createIfNotExists -f="${FILEPATH}"

  _wexTestFileExists "${FILEPATH}"
}
