#!/usr/bin/env bash

frameworkDrupal7SettingsTest() {
  MYSQL_DB_NAME=false
  MYSQL_DB_USER=false
  MYSQL_DB_PASSWORD=false
  wex frameworkDrupal7/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}drupal7/sites/default/settings.php
  # Eval response variables.
  wexTestAssertEqual ${MYSQL_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${MYSQL_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${MYSQL_DB_PASSWORD} "mysqlTestPassword"
}
