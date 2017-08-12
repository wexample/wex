#!/usr/bin/env bash

configGetValueTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  value=$(wexample configGetValue ${filePath} "ConfigTestOption")
  # Got the last valid value
  wexampleTestAssertEqual ${value} "two"

  value=$(wexample configGetValue ${filePath} "ConfigTestOptionEqual" " = ")
  wexampleTestAssertEqual ${value} "one"

  value=$(wexample configGetValue ${filePath} "ConfigTestOptionEqual" "=")
  # Got the last valid value
  wexampleTestAssertEqual ${value} "two"
}
