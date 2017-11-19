#!/usr/bin/env bash

fileJsonReadValueTest() {
  VALUE=$(wex file/jsonReadValue -f="${_TEST_RUN_DIR_SAMPLES}jsonSample.json" -k="simpleValue")
  wexampleTestAssertEqual "${VALUE}" "value"
}
