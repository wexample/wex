#!/usr/bin/env bash

frameworkSettingsTest() {
  websiteTypes=('drupal7' 'symfony3' 'wordpress4')

  # For each type.
  for websiteType in "${websiteTypes[@]}"
  do :
    SITE_DB_HOST=false
    SITE_DB_NAME=false
    SITE_DB_USER=false
    SITE_DB_PASSWORD=false

    wex framework/settings -d=${_TEST_RUN_DIR_SAMPLES}${websiteType}"/"

    wexampleTestAssertEqual ${SITE_DB_HOST} "mysqlTestHost"
    wexampleTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
    wexampleTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
    wexampleTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
  done
}
