#!/usr/bin/env bash

frameworkWordpress4SettingsTest() {
  SITE_DB_NAME=false
  SITE_DB_USER=false
  SITE_DB_PASSWORD=false
  wex frameworkWordpress4/settings -d=${_TEST_RUN_DIR_SAMPLES}wordpress4/wp-config.php
  # Eval response variables.
  wexampleTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
  wexampleTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
  wexampleTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
}
