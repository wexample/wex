#!/usr/bin/env bash

drupal7SettingsTest() {
  wexample drupal7Settings ${_TEST_RUN_DIR_SAMPLES}drupal7/sites/default/settings.php
  # Eval response variables.
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_DRUPAL_7_SETTINGS_PASSWORD} "mysqlTestPassword"
}
