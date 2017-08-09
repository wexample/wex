#!/usr/bin/env bash

silex1SettingsTest() {
  wexample silex1Settings ${_TEST_RUN_DIR_SAMPLES}silex1/config/config.json "test"
  # Eval response variables.
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_SILEX_1_SETTINGS_PASSWORD} "mysqlTestPassword"
}
