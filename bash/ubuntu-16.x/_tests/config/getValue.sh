#!/usr/bin/env bash

configGetValueTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOption")
  # Got the last valid value
  wexampleTestAssertEqual ${value} "two"

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s=" = ")
  wexampleTestAssertEqual ${value} "one"

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s="=")
  # Got the last valid value
  wexampleTestAssertEqual ${value} "two"

  # Reset
  git checkout HEAD -- ${filePath}
}
