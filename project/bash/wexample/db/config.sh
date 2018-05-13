#!/usr/bin/env bash

dbConfig() {
  # Load framework settings
  wex framework/settings -d=./project/

  # No settings found from framework.
  if [ "${SITE_DB_NAME}" == "" ];then
  . .wex

  local DB_TYPE=$(wex db/detect)

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${NAME}_${DB_TYPE}
  export SITE_DB_PORT=5432
  export SITE_DB_NAME=${NAME}
  export SITE_DB_USER=root
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  local DB_CONFIG=''
  DB_CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  DB_CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  DB_CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  DB_CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  DB_CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${DB_CONFIG}
  fi
}