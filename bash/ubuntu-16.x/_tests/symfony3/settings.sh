#!/usr/bin/env bash

symfony3SettingsTest() {
  WEBSITE_SETTINGS_DATABASE=false
  WEBSITE_SETTINGS_USERNAME=false
  WEBSITE_SETTINGS_PASSWORD=false
  wex symfony3/settings ${_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_PASSWORD} "mysqlTestPassword"
}
