#!/usr/bin/env bash

mysqlConfig() {

  wex service/templates -s=mysql -e=cnf.json

  . .wex

  # Load framework settings
  # Old feature : wex framework/settings -d=./project/

  local MYSQL_CONFIG=''
  MYSQL_CONFIG+="\nMYSQL_DB_HOST="${NAME}_mysql
  MYSQL_CONFIG+="\nMYSQL_DB_PORT="3306
  MYSQL_CONFIG+="\nMYSQL_DB_NAME="${NAME}
  MYSQL_CONFIG+="\nMYSQL_DB_USER="root
  MYSQL_CONFIG+="\nMYSQL_DB_PASSWORD=thisIsAReallyNotSecurePassword!"

  echo ${MYSQL_CONFIG}

  # Create connexion file info
  local DB_CONNECTION_FILE=./tmp/mysql.cnf

  echo '[client]' > ${DB_CONNECTION_FILE}
  echo 'user = "'${MYSQL_DB_USER}'"' >> ${DB_CONNECTION_FILE}
  echo 'password = "'${MYSQL_DB_PASSWORD}'"' >> ${DB_CONNECTION_FILE}
  echo 'host = "'${NAME}_mysql'"' >> ${DB_CONNECTION_FILE}
}
