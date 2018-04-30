#!/usr/bin/env bash

frameworkDrupal7SettingsTest() {
  SITE_DB_NAME=false
  SITE_DB_USER=false
  SITE_DB_PASSWORD=false
  wex frameworkDrupal7/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}drupal7/sites/default/settings.php
  # Eval response variables.
  wexTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
  wexTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
  wexTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
}
