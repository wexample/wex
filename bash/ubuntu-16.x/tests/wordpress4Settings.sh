#!/usr/bin/env bash

wordpress4SettingsTest() {
  wexample wordpress4Settings ${_TEST_RUN_DIR_SAMPLES}wordpress4/wp-config.php
  # Eval response variables.
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_DATABASE} "mysqlTestDataBase"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_USERNAME} "mysqlTestUserName"
  wexampleTestAssertEqual ${WEX_WORDPRESS_4_SETTINGS_PASSWORD} "mysqlTestPassword"
}
