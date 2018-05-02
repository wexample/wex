#!/usr/bin/env bash

dbConfig() {
  # TODO : Handle framework detection

  . .wex

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${NAME}_postgres
  export SITE_DB_PORT=5432
  export SITE_DB_NAME=${NAME}
  export SITE_DB_USER=default
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  local POSTGRES_CONFIG=''
  POSTGRES_CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  POSTGRES_CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  POSTGRES_CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  POSTGRES_CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  POSTGRES_CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${POSTGRES_CONFIG}
}