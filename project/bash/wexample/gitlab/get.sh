#!/usr/bin/env bash

gitlabGetArgs() {
  _ARGUMENTS=(
    [0]='query q "Query path" true'
  )
}

gitlabGet() {
  # Load Gitlab token for current user
  . ${WEX_DIR_ROOT}../.env

  curl -s ${WEX_GITLAB_URL}${QUERY}"?private_token=${GITLAB_TOKEN}"
}
