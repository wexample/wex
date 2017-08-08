#!/usr/bin/env bash

_TEST_ARGUMENTS=("${_TEST_RUN_DIR_SAMPLES}silex1Settings.json" "test")

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_PASSWORD} "mysqlTestPassword"
}
