#!/usr/bin/env bash

postgresConfig() {
  # Create ini file.
  . ${WEX_DIR_ROOT}services/mysql/config.sh
  local ACCESS=($(mysqlConfigAccess))
  local POSTGRES_CONFIG=''

  POSTGRES_CONFIG+="\nPOSTGRES_DB_HOST="${ACCESS[0]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_PORT="${ACCESS[1]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_NAME="${ACCESS[2]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_USER="${ACCESS[3]}
  POSTGRES_CONFIG+="\nPOSTGRES_DB_PASSWORD=${ACCESS[4]}"

  echo ${POSTGRES_CONFIG}
}
