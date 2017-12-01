#!/usr/bin/env bash

mysqlLoginCommand() {
  # Export default credentials if not found in framework.
  wex wexample::db/credentialsDefault

  wex framework/settings

  echo -hmysql -u${SITE_DB_USER} -p${SITE_DB_PASSWORD} ${SITE_DB_NAME}
}
