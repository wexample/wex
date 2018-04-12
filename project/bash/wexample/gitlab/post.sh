#!/usr/bin/env bash

gitlabPostArgs() {
  _ARGUMENTS=(
    [0]='query q "Query path" true'
    [1]='data d "Post data" true'
  )
}

gitlabPost() {
  local WEX_GITLAB_URL="http://gitlab.wexample.com/api/v4/"
  # Load Gitlab token for current user
  . ${WEX_DIR_ROOT}../.env

  curl -d ${DATA} -X POST ${WEX_GITLAB_URL}${QUERY}"?private_token=${GITLAB_TOKEN}"
}
