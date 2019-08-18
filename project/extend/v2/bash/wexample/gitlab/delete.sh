#!/usr/bin/env bash

gitlabDeleteArgs() {
  _ARGUMENTS=(
    [0]='path_query p "Path" false'
    [1]='url u "Gitlab repo url" false'
    [2]='token t "Gitlab token" false'
  )
}

gitlabDelete() {
  # Build path.
  local BASE_URL=$(wex gitlab/baseUrl -p=${PATH_QUERY} -u=${URL} -t=${TOKEN})
  # Post
  curl -X DELETE ${BASE_URL}
}
