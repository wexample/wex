#!/usr/bin/env bash

frameworkSymfony3SettingsTest() {
  MYSQL_DB_NAME=false
  MYSQL_DB_USER=false
  MYSQL_DB_PASSWORD=false
  wex frameworkSymfony3/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexTestAssertEqual ${MYSQL_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${MYSQL_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${MYSQL_DB_PASSWORD} "mysqlTestPassword"
}
