#!/usr/bin/env bash

frameworkWordpress4SettingsTest() {
  MYSQL_DB_NAME=false
  MYSQL_DB_USER=false
  MYSQL_DB_PASSWORD=false
  wex frameworkWordpress4/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}wordpress4/wp-config.php
  # Eval response variables.
  wexTestAssertEqual ${MYSQL_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${MYSQL_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${MYSQL_DB_PASSWORD} "mysqlTestPassword"
}
