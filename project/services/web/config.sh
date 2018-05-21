#!/usr/bin/env bash

webConfig() {
  # php.ini
  wex service/templates -s=php -e=ini
  # apache.conf
  wex service/templates -s=apache -e=conf

  # Create ini file.
  . ${WEX_DIR_ROOT}services/mysql/config.sh
  local ACCESS=($(mysqlConfigAccess))
  local INI=./tmp/php.env.ini
  local SITE_ENV=$(wex site/env)

  echo '; Auto generated configuration' > ${INI}
  echo '[site]' >> ${INI}
  echo 'SITE_ENV = "'${SITE_ENV}'"' >> ${INI}
  echo 'DOMAIN_MAIN = "'${DOMAIN_MAIN}'"' >> ${INI}
  echo '[mysql]' >> ${INI}
  echo 'MYSQL_DB_HOST = "'${ACCESS[0]}'"' >> ${INI}
  echo 'MYSQL_DB_PORT = "'${ACCESS[1]}'"' >> ${INI}
  echo 'MYSQL_DB_NAME = "'${ACCESS[2]}'"' >> ${INI}
  echo 'MYSQL_DB_USER = "'${ACCESS[3]}'"' >> ${INI}
  echo 'MYSQL_DB_PASSWORD = "'${ACCESS[4]}'"' >> ${INI}

  echo "\nSITE_CONTAINER=web"
}
