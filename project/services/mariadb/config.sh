#!/usr/bin/env bash

mariadbConfig() {
  wex service/templates -s=mariadb -e=cnf.json

  # Create ini file.
  . ${WEX_DIR_ROOT}services/mysql/config.sh
  local ACCESS=($(mysqlConfigAccess))
  local MARIADB_CONFIG=''

  MARIADB_CONFIG+="\nMARIADB_DB_HOST="${ACCESS[0]}
  MARIADB_CONFIG+="\nMARIADB_DB_PORT="${ACCESS[1]}
  MARIADB_CONFIG+="\nMARIADB_DB_NAME="${NAME}_mariadb
  MARIADB_CONFIG+="\nMARIADB_DB_USER="${ACCESS[3]}
  MARIADB_CONFIG+="\nMARIADB_DB_PASSWORD=${ACCESS[4]}"

  echo ${MARIADB_CONFIG}
}
