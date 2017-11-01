#!/usr/bin/env bash

wexampleSiteScpUploadArgs() {
 _ARGUMENTS=(
   [0]='dir d "Local root site directory" true'
   [1]='file f "Local file to upload" true'
 )
}

wexampleSiteScpUpload() {
  wex wexample/siteGetDeployCredentials -d=${DIR}
  scp -P${DEPLOY_PORT} ${FILE} ${DEPLOY_USER}@${DEPLOY_IPV4}:/home/${DEPLOY_USER}
}
