#!/usr/bin/env bash

gitlabPostArgs() {
  _ARGUMENTS=(
    [0]='path_query p "Path" false'
    [1]='url u "Gitlab repo url" false'
    [2]='token t "Gitlab token" false'
    [3]='data d "Post data" false'
  )
}

gitlabPost() {
  # Build path.
  local BASE_URL=$(wex gitlab/baseUrl -p=${PATH_QUERY} -u=${URL} -t=${TOKEN})
  local OPTIONS=''

  if [ "${DATA}" != "" ];then
    OPTIONS="-d ${DATA}"
  fi

  # Post
  curl ${OPTIONS} -X POST ${BASE_URL}
}
