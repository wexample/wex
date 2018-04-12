#!/usr/bin/env bash

frameworkSymfony3SettingsTest() {
  SITE_DB_NAME=false
  SITE_DB_USER=false
  SITE_DB_PASSWORD=false
  wex frameworkSymfony3/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
}
