#!/usr/bin/env bash

backupCreateArgs() {
  _AS_NON_SUDO=false
  _DEPENDENCIES=(
    'zip'
  )
  _SUDO_REASON="Store a file in /var/www/backup dir"
}

backupCreate() {
  local BACKUP_DIR=/var/www/backup
  mkdir -p "${BACKUP_DIR}"

  . tmp/config

  cd ../

  local ZIP_NAME="${BACKUP_DIR}/${SITE_NAME}-${SITE_ENV}-$(wex date/timeFileName).zip"
  zip -r "${ZIP_NAME}" "${SITE_NAME}" -x '*.git*'

  echo "${ZIP_NAME}"
}