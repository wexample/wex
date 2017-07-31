#!/usr/bin/env bash

arguments() {
  arguments=( "${_TEST_RUN_DIR_CURRENT}samples/wordPress4Settings.php" )
}

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_PASSWORD} "mysqlTestPassword"
}
