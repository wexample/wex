#!/usr/bin/env bash

arguments() {
  arguments=( "${_TEST_RUN_DIR_CURRENT}samples/drupal7Settings.php" )
}

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_PASSWORD} "mysqlTestPassword"
}
