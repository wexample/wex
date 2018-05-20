#!/usr/bin/env bash

wordpressConfig() {
  # php.ini
  wex service/templates -s=php -e=ini
  # apache.conf
  wex service/templates -s=apache -e=conf
  local MYSQL_DB_HOST=''

  . ${WEX_DIR_ROOT}services/mysql/config.sh
  local ACCESS=($(mysqlConfigAccess))

  local CONFIG

  # Create connexion file info
  local INI=./tmp/php.env.ini

  echo '[mysql]' > ${INI}
  echo 'MYSQL_DB_HOST = "'${ACCESS[0]}'"' >> ${INI}
  echo 'MYSQL_DB_PORT = "'${ACCESS[1]}'"' >> ${INI}
  echo 'MYSQL_DB_NAME = "'${ACCESS[2]}'"' >> ${INI}
  echo 'MYSQL_DB_USER = "'${ACCESS[3]}'"' >> ${INI}
  echo 'MYSQL_DB_PASSWORD = "'${ACCESS[4]}'"' >> ${INI}

  # Set as main site container.
  echo "\nSITE_CONTAINER=wordpress"
}
