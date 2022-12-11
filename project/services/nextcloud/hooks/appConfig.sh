#!/usr/bin/env bash

nextcloudAppConfig() {

  echo -e "\nSITE_CONTAINER=nextcloud"

  . .wex

  echo -e "\nNEXTCLOUD_VERSION=${NEXTCLOUD_VERSION}"

  # Export default credentials if not found in framework.
  export MYSQL_DB_HOST=${NAME}_nextcloud
  export MYSQL_DB_PORT=3306
  export MYSQL_DB_NAME=${NAME}
  export MYSQL_DB_USER=root
  export MYSQL_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  local NEXTCLOUD_CONFIG=''
  echo -e "\nMYSQL_DB_HOST="${MYSQL_DB_HOST} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMYSQL_DB_PORT="${MYSQL_DB_PORT} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMYSQL_DB_NAME="${MYSQL_DB_NAME} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMYSQL_DB_USER="${MYSQL_DB_USER} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nMYSQL_DB_PASSWORD="${MYSQL_DB_PASSWORD} >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
