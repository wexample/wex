#!/usr/bin/env bash

gitlabDeleteArgs() {
  _ARGUMENTS=(
    [0]='query q "Query path" true'
  )
}

gitlabDelete() {
  local WEX_GITLAB_URL="http://gitlab.wexample.com/api/v4/"
  # Load Gitlab token for current user
  . ${WEX_DIR_ROOT}../.env

  curl -X DELETE ${WEX_GITLAB_URL}${QUERY}"?private_token=${GITLAB_TOKEN}"
}
