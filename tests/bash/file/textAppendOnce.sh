#!/usr/bin/env bash

fileTextAppendOnceTest() {
  local FILEPATH
  local ORIGINAL
  local CONFIG_VALUE
  local CONFIG_KEY
  local CONFIG_TEST
  local INSERTED

  FILEPATH=$(_wexTestSampleInit fileTextSample1.txt)

  ORIGINAL=$(<${FILEPATH})

  # Try to append a line which exists
  wex-exec file/textAppendOnce -f="${FILEPATH}" -l="[INNER LINE]"
  _wexTestSampleDiff fileTextSample1.txt false "Trying insert existing line"

  # Try to append a line which looks like another on but not exactly
  wex-exec file/textAppendOnce -f="${FILEPATH}" -l="\n[INNER LINE"
  _wexTestSampleDiff fileTextSample1.txt true "Line inserted"

  # Try to append config line
  CONFIG_VALUE="true; # With an unsupported comment"
  CONFIG_KEY="SuperConf"
  CONFIG_TEST="${CONFIG_KEY} = ${CONFIG_VALUE}"

  wex-exec file/textAppendOnce -f="${FILEPATH}" -l="${CONFIG_TEST}"

  INSERTED=$(wex-exec default::config/getValue -f="${FILEPATH}" -k="${CONFIG_KEY}" -s=" = ")
  _wexTestAssertEqual "${INSERTED}" "${CONFIG_VALUE}"
}
