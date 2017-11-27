#!/usr/bin/env bash

mysqlLoginCommand() {
  wex framework/settings
  echo -hmysql -u${SITE_DB_USER} -p${SITE_DB_PASSWORD} ${SITE_DB_NAME}
}
