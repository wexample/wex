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

    wex framework/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}${websiteType}"/"

    wexTestAssertEqual ${SITE_DB_HOST} "mysqlTestHost"
    wexTestAssertEqual ${SITE_DB_NAME} "mysqlTestDataBase"
    wexTestAssertEqual ${SITE_DB_USER} "mysqlTestUserName"
    wexTestAssertEqual ${SITE_DB_PASSWORD} "mysqlTestPassword"
  done
}
