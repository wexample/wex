#!/usr/bin/env bash

fileDownloadArgs() {
  _ARGUMENTS=(
    [0]='scp_username u "SCP Username" false'
    [1]='scp_private_key pk "SCP Private key" false'
    [2]='environment e "Environment to transfer from" true'
    [3]='file f "Remote file to download" true'
    [4]='dir_to d "Local destination folder" false'
  )
}

fileDownload() {
  if [ -z "${DIR_TO+x}" ]; then
    DIR_TO=./
  fi;

  wex env/credentials -e=${ENVIRONMENT} -u=${SCP_USERNAME} -pk=${SCP_PRIVATE_KEY}
  # Download file
  scp -i${SITE_PRIVATE_KEY} -P${SITE_PORT} ${SITE_USERNAME}@${SITE_IPV4}:${FILE} ${DIR_TO}
  # Prevent to set credentials globally
  wex env/credentialsClear
}
