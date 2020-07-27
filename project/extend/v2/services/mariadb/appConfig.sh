#!/usr/bin/env bash

mariadbAppConfig() {
  wex config/bindFiles -s=mariadb -e=cnf.json

  # Create ini file.
  . ${WEX_DIR_SERVICES}mysql/appConfig.sh
  local ACCESS=($(mysqlAppConfigAccess))
  local MARIADB_CONFIG=''

  echo -e "\nMARIADB_DB_HOST="${ACCESS[0]} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMARIADB_DB_PORT="${ACCESS[1]} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMARIADB_DB_NAME="${NAME}_mariadb >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMARIADB_DB_USER="${ACCESS[3]} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMARIADB_DB_PASSWORD=${ACCESS[4]}" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
