#!/usr/bin/env bash

otraAppConfig() {
  # php.ini
  wex config/bindFiles -s=php -e=ini
  # apache.conf
  wex config/bindFiles -s=apache -e=conf

  . .wex

  echo -e "\nOTRA_VERSION=${OTRA_VERSION}"

  # Create ini file.
  . ${WEX_DIR_SERVICES}mysql/hooks/appConfig.sh
  local ACCESS=($(mysqlAppConfigAccess))
  local INI=./tmp/php.env.ini
  local SITE_ENV=$(wex app/env)

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

  echo -e "\nSITE_CONTAINER=otra" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
