#!/usr/bin/env bash

fileJsonReadValueTest() {
  wex file/jsonReadValue -f="${_TEST_RUN_DIR_SAMPLES}/jsonSample.json" -k="nested > thirdNested > leaf"
}
