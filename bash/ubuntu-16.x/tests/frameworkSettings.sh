#!/usr/bin/env bash

frameworkSettingsTest() {
  websiteTypes=('drupal7' 'silex1' 'symfony3' 'wordpress4')

  # For each type.
  for websiteType in "${websiteTypes[@]}"
  do :
    WEBSITE_SETTINGS_HOST=false
    WEBSITE_SETTINGS_DATABASE=false
    WEBSITE_SETTINGS_USERNAME=false
    WEBSITE_SETTINGS_PASSWORD=false

    wexample frameworkSettings ${_TEST_RUN_DIR_SAMPLES}${websiteType}"/"

    wexampleTestAssertEqual ${WEBSITE_SETTINGS_HOST} "mysqlTestHost"
    wexampleTestAssertEqual ${WEBSITE_SETTINGS_DATABASE} "mysqlTestDataBase"
    wexampleTestAssertEqual ${WEBSITE_SETTINGS_USERNAME} "mysqlTestUserName"
    wexampleTestAssertEqual ${WEBSITE_SETTINGS_PASSWORD} "mysqlTestPassword"
  done
}
