#!/usr/bin/env bash

mysqlConfig() {
  wex service/templates -s=mysql -e=cnf

  # Get site name from wex.json.
  SITE_NAME=$(wex site/config -k=name)

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${SITE_NAME}_mysql
  export SITE_DB_PORT=3306
  export SITE_DB_NAME=${SITE_NAME}
  export SITE_DB_USER=root
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  # Load framework settings
  wex framework/settings -d=./project/

  local MYSQL_CONFIG=''
  MYSQL_CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  MYSQL_CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  MYSQL_CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  MYSQL_CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  MYSQL_CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${MYSQL_CONFIG}
}
