#!/usr/bin/env bash

nextcloudConfig() {
  wex service/templates -s=nextcloud -e=cnf.json

  . .wex

  # Export default credentials if not found in framework.
  export SITE_DB_HOST=${NAME}_nextcloud
  export SITE_DB_PORT=3306
  export SITE_DB_NAME=${NAME}
  export SITE_DB_USER=root
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"

  local NEXTCLOUD_CONFIG=''
  NEXTCLOUD_CONFIG+="\nSITE_DB_HOST="${SITE_DB_HOST}
  NEXTCLOUD_CONFIG+="\nSITE_DB_PORT="${SITE_DB_PORT}
  NEXTCLOUD_CONFIG+="\nSITE_DB_NAME="${SITE_DB_NAME}
  NEXTCLOUD_CONFIG+="\nSITE_DB_USER="${SITE_DB_USER}
  NEXTCLOUD_CONFIG+="\nSITE_DB_PASSWORD="${SITE_DB_PASSWORD}

  echo ${NEXTCLOUD_CONFIG}
}
