#!/usr/bin/env bash

mysqlLoginCommand() {
  # Load credentials stored into config
  wex site/configLoad

  echo -hmysql -u${SITE_DB_USER} -p${SITE_DB_PASSWORD} ${SITE_DB_NAME}
}
