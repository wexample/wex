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
  wex env/credentials -e=${ENVIRONMENT} -u=${SCP_USERNAME} -pk=${SCP_PRIVATE_KEY}
  # Copy to given location
  scp -r -i${SITE_PRIVATE_KEY} -P${SITE_PORT} ${FILE} ${SITE_USERNAME}@${SITE_IPV4}:${SITE_PATH_ROOT}${DIR_TO}
  # Give www-data permissions (files may be a part of website)
  wex wexample::ssh/exec -e=${ENVIRONMENT} -s="chown -R www-data:www-data ${SITE_PATH_ROOT}${DIR_TO}"
  # Prevent to set credentials globally
  wex env/credentialsClear
}
