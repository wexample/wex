#!/usr/bin/env bash

fileUploadArgs() {
  _ARGUMENTS=(
    [0]='scp_username u "SCP Username" false'
    [1]='scp_private_key pk "SCP Private key file" false'
    [2]='environment e "Environment to transfer to" true'
    [3]='file f "Local file or folder to upload" true'
    [4]='dir_to d "Destination folder, relative to site root (/var/www/name/)" false'
  )
}

fileUpload() {
  local ENV=$(wex text/uppercase -t="${ENVIRONMENT}")
  # Need site path
  wex config/load
  local REMOTE_SITE_PATH_ROOT=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SITE_NAME}/

  wexampleSiteInitLocalVariables
  . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

  # Get value
  local SSH_USER=$(eval 'echo ${'${ENV}'_SSH_USER}')
  local SSH_HOST=$(eval 'echo ${'${ENV}'_SSH_HOST}')
  local SSH_PORT=$(eval 'echo ${'${ENV}'_SSH_PORT}')
  local SSH_PRIVATE_KEY=$(eval 'echo ${'${ENV}'_SSH_PRIVATE_KEY}')

  if [ "${SSH_PORT}" == "" ];then
    SSH_PORT=22
  fi

  # Copy to given location
  scp -r -i${SSH_PRIVATE_KEY} -P${SSH_PORT} ${FILE} ${SSH_USER}@${SSH_HOST}:${REMOTE_SITE_PATH_ROOT}${DIR_TO}
  # Give www-data permissions (files may be a part of website)
  wex wexample::remote/exec -e=${ENVIRONMENT} -s="chown -R www-data:www-data ${REMOTE_SITE_PATH_ROOT}${DIR_TO}"
}
