#!/usr/bin/env bash

frameworkWordpress4SettingsTest() {
  SITE_DB_NAME=false
  SITE_DB_USER=false
  SITE_DB_PASSWORD=false
  wex frameworkWordpress4/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}wordpress4/wp-config.php
  # Eval response variables.
  wexTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
}
