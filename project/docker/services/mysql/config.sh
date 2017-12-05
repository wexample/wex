#!/usr/bin/env bash

mysqlConfig() {

  # Export default credentials if not found in framework.
  wex wexample::db/credentialsDefault
  # Load framework settings
  wex framework/settings -d=${CONTAINER_PATH_ROOT}

  MYSQL_CONFIG=''
  MYSQL_CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  MYSQL_CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  MYSQL_CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  MYSQL_CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  MYSQL_CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${MYSQL_CONFIG}
}
