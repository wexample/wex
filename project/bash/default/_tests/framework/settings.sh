#!/usr/bin/env bash

frameworkSettingsTest() {
  websiteTypes=('drupal7' 'symfony3' 'wordpress4')

  # For each type.
  for websiteType in "${websiteTypes[@]}"
  do :
    MYSQL_DB_HOST=false
    MYSQL_DB_NAME=false
    MYSQL_DB_USER=false
    MYSQL_DB_PASSWORD=false

    wex framework/settings -d=${WEX_TEST_RUN_DIR_SAMPLES}${websiteType}"/"

    wexTestAssertEqual ${MYSQL_DB_HOST} "mysqlTestHost"
    wexTestAssertEqual ${MYSQL_DB_NAME} "mysqlTestDataBase"
    wexTestAssertEqual ${MYSQL_DB_USER} "mysqlTestUserName"
    wexTestAssertEqual ${MYSQL_DB_PASSWORD} "mysqlTestPassword"
  done
}
