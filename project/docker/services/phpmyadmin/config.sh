#!/usr/bin/env bash

phpmyadminConfig() {
  wex service/templates -s=php -e=ini

  . .wex

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${NAME}_mysql
  export SITE_DB_PORT=3306
  export SITE_DB_NAME=${NAME}
  export SITE_DB_USER=root
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  # Load framework settings
  wex framework/settings -d=./project/

  local CONFIG=''
  CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${CONFIG}
}
