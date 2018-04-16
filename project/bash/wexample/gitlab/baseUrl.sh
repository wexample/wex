#!/usr/bin/env bash

gitlabBaseUrlArgs() {
  _ARGUMENTS=(
    [0]='path_query p "Path" false'
    [1]='url u "Gitlab repo url" false'
    [2]='token t "Gitlab token" false'
  )
}

gitlabBaseUrl() {
  local GITLAB_URL=${URL};
  local GITLAB_TOKEN=${TOKEN};

  if [ "${GITLAB_URL}" == "" ]; then
    local GITLAB_URL=$(wex wexample::var/localGet -n=GITLAB_URL_DEFAULT -ask="Gitlab repository url" -d="${WEX_GITLAB_URL}")
    local GITLAB_TOKEN=$(wex wexample::var/localGet -n=GITLAB_TOKEN_DEFAULT -ask="Gitlab token")
  fi;

  echo "http://"${GITLAB_URL}"/api/v4/"${PATH_QUERY}"?private_token=${GITLAB_TOKEN}&"
}
