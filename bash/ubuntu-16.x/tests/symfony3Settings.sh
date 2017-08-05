#!/usr/bin/env bash

_TEST_ARGUMENTS=("${_TEST_RUN_DIR_SAMPLES}symfony3Settings.yml")

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_PASSWORD} "mysqlTestPassword"
}
