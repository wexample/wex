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

  # Load from data storage
  if [ "${GITLAB_URL}" == "" ]; then
    wexampleSiteInitLocalVariables
    . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

    if [ "${GITLAB_URL_DEFAULT}" != "" ] && [ "${GITLAB_TOKEN_DEFAULT}" != "" ]; then
      GITLAB_URL=${GITLAB_URL_DEFAULT}
      GITLAB_TOKEN=${GITLAB_TOKEN_DEFAULT}
    fi
  fi

  # Ask user and store data
  if [ "${GITLAB_URL}" == "" ] || [ "${GITLAB_TOKEN}" == "" ]; then
    local GITLAB_URL=$(wex wexample::var/localGet -s -n=GITLAB_URL_DEFAULT -ask="Gitlab repository url" -d="${WEX_GITLAB_URL}")
    local GITLAB_TOKEN=$(wex wexample::var/localGet -s -n=GITLAB_TOKEN_DEFAULT -ask="Gitlab token")
  fi;

  echo "http://"${GITLAB_URL}"/api/v4/"${PATH_QUERY}"?private_token=${GITLAB_TOKEN}&"
}
