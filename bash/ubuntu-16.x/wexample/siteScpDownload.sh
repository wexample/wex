#!/usr/bin/env bash

wexampleSiteScpDownloadArgs() {
 _ARGUMENTS=(
   [0]='dir d "Local root site directory" true'
   [1]='file f "Local file to upload" true'
 )
}

wexampleSiteScpDownload() {
  wex wexample/siteGetDeployCredentials.sh -d=${DIR}
  scp -P${DEPLOY_PORT} ${DEPLOY_USER}@${DEPLOY_IPV4}:/home/${DEPLOY_USER} ${FILE}
}
