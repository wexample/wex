#!/usr/bin/env bash

scpDownloadArgs() {
  _ARGUMENTS=(
    [0]='username u "SCP Username" true'
    [1]='dir d "Local root site directory" true'
    [2]='file f "Local file to upload" true'
  )
}

scpDownload() {
  wex wexample::site/deployCredentials -d=${DIR}
  scp -P${DEPLOY_PORT} ${USERNAME}@${DEPLOY_IPV4}:/home/${USERNAME} ${FILE}
}
