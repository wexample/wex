#!/usr/bin/env bash

mysqlConfig() {

  wex service/templates -s=mysql -e=cnf.json

  # TODO Use wex db/config

  . .wex

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${NAME}_mysql
  export SITE_DB_PORT=3306
  export SITE_DB_NAME=${NAME}
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

  # Create connexion file info
  local DB_CONNECTION_FILE=./tmp/mysql.cnf

  echo '[client]' > ${DB_CONNECTION_FILE}
  echo 'user = "'${SITE_DB_USER}'"' >> ${DB_CONNECTION_FILE}
  echo 'password = "'${SITE_DB_PASSWORD}'"' >> ${DB_CONNECTION_FILE}
  echo 'host = "'${NAME}_mysql'"' >> ${DB_CONNECTION_FILE}
}
