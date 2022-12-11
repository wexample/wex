#!/usr/bin/env bash

webAppConfig() {
  wex config/addTitle -t="Web"
  wex config/setValue -k=SITE_CONTAINER -v=web
  wex config/setValue -k=PROJECT_DIR -v=project

  # php.ini
  wex config/bindFiles -s=php -e=ini
  # apache.conf
  wex config/bindFiles -s=apache -e=conf

  # Create ini file.
  . ${WEX_DIR_SERVICES}mysql/hooks/appConfig.sh
  local ACCESS=($(mysqlAppConfigAccess))
  local INI=./tmp/php.env.ini
  local SITE_ENV=$(wex app/env)

  _wexLog "Creating PHP ${INI}"

  echo -e "; Auto generated configuration" > ${INI}

  echo -e "\n\n\n[site]" >> ${INI}
  wex config/setValue -k=SITE_ENV -v="${SITE_ENV}" -f=${INI}

  echo -e "\n\n\n[mysql]" >> ${INI}
  wex config/setValue -k=MYSQL_DB_HOST -v=${ACCESS[0]} -f=${INI}
  wex config/setValue -k=MYSQL_DB_PORT -v=${ACCESS[1]} -f=${INI}
  wex config/setValue -k=MYSQL_DB_NAME -v=${ACCESS[2]} -f=${INI}
  wex config/setValue -k=MYSQL_DB_USER -v=${ACCESS[3]} -f=${INI}
  wex config/setValue -k=MYSQL_DB_PASSWORD -v='"'${ACCESS[4]}'"' -f=${INI}
}
