#!/usr/bin/env bash

frameworkSymfony3SettingsTest() {
  SITE_DB_NAME=false
  SITE_DB_USER=false
  SITE_DB_PASSWORD=false
  wex frameworkSymfony3/settings -d=${_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexampleTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
  wexampleTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
  wexampleTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
}
