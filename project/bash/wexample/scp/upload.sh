#!/usr/bin/env bash

scpUploadArgs() {
  _ARGUMENTS=(
    [0]='scp_username u "SCP Username" false'
    [1]='scp_private_key pk "SCP Private key" false'
    [2]='environment e "Environment to transfer to" true'
    [3]='file f "Local file to upload" true'
    [4]='dir_to d "Destination folder" true'
  )
}

scpUpload() {
  wex env/credentials -e=${ENVIRONMENT} -u=${SCP_USERNAME} -pk=${SCP_PRIVATE_KEY}
  # Copy to given location
  scp -i${SITE_PRIVATE_KEY} -P${SITE_PORT} ${FILE} ${SITE_USERNAME}@${SITE_IPV4}:${DIR_TO}
  # Prevent to set credentials globally
  wex env/credentialsClear
}
