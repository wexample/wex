#!/usr/bin/env bash

symfony3SettingsTest() {
  wexample symfony3Settings ${_TEST_RUN_DIR_SAMPLES}symfony3/app/config/parameters.yml
  # Eval response variables.
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_SYMFONY_3_SETTINGS_PASSWORD} "mysqlTestPassword"
}
