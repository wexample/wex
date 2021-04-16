#!/usr/bin/env bash

postgresConfig() {
  # Create ini file.
  . ${WEX_DIR_ROOT}services/mysql/config.sh
  local ACCESS=($(mysqlConfigAccess))
  local POSTGRES_CONFIG=''

  . .wex

  POSTGRES_CONFIG+="\nPOSTGRES_DB_HOST="${ACCESS[0]}_postgres
  POSTGRES_CONFIG+="\nPOSTGRES_DB_PORT=5432"
  POSTGRES_CONFIG+="\nPOSTGRES_DB_NAME="${ACCESS[2]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_USER="${ACCESS[3]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_PASSWORD=${ACCESS[4]}"

  echo ${POSTGRES_CONFIG}

  echo "\nPOSTGRES_VERSION=${POSTGRES_VERSION}"
}
