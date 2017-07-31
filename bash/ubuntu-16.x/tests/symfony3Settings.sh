#!/usr/bin/env bash

arguments() {
  arguments=( "${_TEST_RUN_DIR_CURRENT}samples/symfony3Settings.yml" )
}

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_PASSWORD} "mysqlTestPassword"
}
