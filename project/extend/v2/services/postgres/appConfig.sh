#!/usr/bin/env bash

postgresAppConfig() {
  # Create ini file.
  . ${WEX_DIR_ROOT}services/mysql/appConfig.sh
  local ACCESS=($(mysqlAppConfigAccess))
  local POSTGRES_CONFIG=''

  . .wex

  echo -e "\nPOSTGRES_DB_HOST="${SITE_NAME_INTERNAL}_postgres >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nPOSTGRES_DB_PORT=5432" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nPOSTGRES_DB_NAME="${ACCESS[2]} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nPOSTGRES_DB_USER="${ACCESS[3]} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nPOSTGRES_DB_PASSWORD=${ACCESS[4]}" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nPOSTGRES_VERSION=${POSTGRES_VERSION}" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
