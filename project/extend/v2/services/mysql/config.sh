#!/usr/bin/env bash

mysqlConfig() {

  wex service/templates -s=mysql -e=cnf

  . .wex
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Load framework settings
  # Old feature : wex framework/settings -d=./project/

  local ACCESS=($(mysqlConfigAccess))
  local MYSQL_CONFIG=''
  local HOST=${SITE_NAME_INTERNAL}_mysql
  local USER=root
  local PASSWORD="thisIsAReallyNotSecurePassword!"

  MYSQL_CONFIG+="\nMYSQL_DB_HOST="${ACCESS[0]}
  MYSQL_CONFIG+="\nMYSQL_DB_PORT="${ACCESS[1]}
  MYSQL_CONFIG+="\nMYSQL_DB_NAME="${ACCESS[2]}
  MYSQL_CONFIG+="\nMYSQL_DB_USER="${ACCESS[3]}
  MYSQL_CONFIG+="\nMYSQL_DB_PASSWORD=${ACCESS[4]}"

  echo ${MYSQL_CONFIG}

  # Create connexion file info
  local DB_CONNECTION_FILE=./tmp/mysql.cnf

  echo '[client]' > ${DB_CONNECTION_FILE}
  echo 'user = "'${ACCESS[3]}'"' >> ${DB_CONNECTION_FILE}
  echo 'password = "'${ACCESS[4]}'"' >> ${DB_CONNECTION_FILE}
  echo 'host = "'${ACCESS[0]}'"' >> ${DB_CONNECTION_FILE}

  # Expected access level
  chmod 644 ${DB_CONNECTION_FILE}
}

mysqlConfigAccess() {
  local MYSQL_PASSWORD='thisIsAReallyNotSecurePassword!'

  . .wex
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Host
  echo ${SITE_NAME_INTERNAL}_mysql
  # Port
  echo 3306
  # Name
  echo ${NAME}
  # User
  echo root
  # Password
  echo "${MYSQL_PASSWORD}"
}