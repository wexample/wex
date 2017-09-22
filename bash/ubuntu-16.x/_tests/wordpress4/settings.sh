#!/usr/bin/env bash

wordpress4SettingsTest() {
  WEBSITE_SETTINGS_DATABASE=false
  WEBSITE_SETTINGS_USERNAME=false
  WEBSITE_SETTINGS_PASSWORD=false
  wex wordpress4/settings ${_TEST_RUN_DIR_SAMPLES}wordpress4/wp-config.php
  # Eval response variables.
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEBSITE_SETTINGS_PASSWORD} "mysqlTestPassword"
}
