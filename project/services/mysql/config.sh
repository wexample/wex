#!/usr/bin/env bash

mysqlConfig() {

  wex service/templates -s=mysql -e=cnf.json

  . .wex

  # Load framework settings
  # Old feature : wex framework/settings -d=./project/

  local MYSQL_CONFIG=''
  local HOST=${NAME}_mysql
  local USER=root
  local PASSWORD="thisIsAReallyNotSecurePassword!"

  MYSQL_CONFIG+="\nMYSQL_DB_HOST="${HOST}
  MYSQL_CONFIG+="\nMYSQL_DB_PORT="3306
  MYSQL_CONFIG+="\nMYSQL_DB_NAME="${NAME}
  MYSQL_CONFIG+="\nMYSQL_DB_USER="${USER}
  MYSQL_CONFIG+="\nMYSQL_DB_PASSWORD=${PASSWORD}"

  echo ${MYSQL_CONFIG}

  # Create connexion file info
  local DB_CONNECTION_FILE=./tmp/mysql.cnf

  echo '[client]' > ${DB_CONNECTION_FILE}
  echo 'user = "'${USER}'"' >> ${DB_CONNECTION_FILE}
  echo 'password = "'${PASSWORD}'"' >> ${DB_CONNECTION_FILE}
  echo 'host = "'${HOST}'"' >> ${DB_CONNECTION_FILE}
}
