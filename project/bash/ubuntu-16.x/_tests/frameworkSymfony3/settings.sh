#!/usr/bin/env bash

frameworkSymfony3SettingsTest() {
  WEBSITE_SETTINGS_DATABASE=false
  WEBSITE_SETTINGS_USERNAME=false
  WEBSITE_SETTINGS_PASSWORD=false
  wex frameworkSymfony3/settings -d=${_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_PASSWORD} "mysqlTestPassword"
}
