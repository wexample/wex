#!/usr/bin/env bash

_TEST_ARGUMENTS=("${_TEST_RUN_DIR_SAMPLES}wordPress4Settings.php")

verify() {
  # Eval response variables.
  eval ${1}
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_PASSWORD} "mysqlTestPassword"
}
