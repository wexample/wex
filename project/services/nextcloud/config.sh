#!/usr/bin/env bash

nextcloudConfig() {

  echo "\nSITE_CONTAINER=nextcloud"

  . .wex

  # Export default credentials if not found in framework.
  export MYSQL_DB_HOST=${NAME}_nextcloud
  export MYSQL_DB_PORT=3306
  export MYSQL_DB_NAME=${NAME}
  export MYSQL_DB_USER=root
  export MYSQL_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  local NEXTCLOUD_CONFIG=''
  NEXTCLOUD_CONFIG+="\nMYSQL_DB_HOST="${MYSQL_DB_HOST}
  NEXTCLOUD_CONFIG+="\nMYSQL_DB_PORT="${MYSQL_DB_PORT}
  NEXTCLOUD_CONFIG+="\nMYSQL_DB_NAME="${MYSQL_DB_NAME}
  NEXTCLOUD_CONFIG+="\nMYSQL_DB_USER="${MYSQL_DB_USER}
  NEXTCLOUD_CONFIG+="\nMYSQL_DB_PASSWORD="${MYSQL_DB_PASSWORD}

  echo ${NEXTCLOUD_CONFIG}
}
