#!/usr/bin/env bash

scpUploadArgs() {
 _ARGUMENTS=(
   [0]='username u "SCP Username" true'
   [1]='file f "Local file to upload" true'
   [2]='dir_site d "Local root site directory" false'
 )
}

scpUpload() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  wex wexample::site/deployCredentials -d=${DIR_SITE}
  # Copy in user folder
  scp -P${DEPLOY_PORT} ${FILE} ${USERNAME}@${DEPLOY_IPV4}:~/
}
