#!/usr/bin/env bash

_TEST_ARGUMENTS=("${_TEST_RUN_DIR_SAMPLES}drupal7Settings.php")

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_PASSWORD} "mysqlTestPassword"
}
