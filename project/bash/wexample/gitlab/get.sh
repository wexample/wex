#!/usr/bin/env bash

gitlabGetArgs() {
  _ARGUMENTS=(
    [0]='path_query p "Path" true'
    [1]='url u "Gitlab repo url" false'
    [2]='token t "Gitlab token" false'
    [3]='query_string qs "Query string" false'
    [4]='key k "Specific key value" false'
  )
}

gitlabGet() {
  # Build path.
  local BASE_URL=$(wex gitlab/baseUrl -p=${PATH_QUERY} -u=${URL} -t=${TOKEN})
  # Get
  local JSON=$(curl -s ${BASE_URL}${QUERY_STRING})

  if [ ! -z "${KEY+x}" ]; then
    echo -e ${JSON} | sed -E 's/.*'${KEY}'":"([^"]*)".*$/\1/'
  else
    # Return full JSON
    echo ${JSON}
  fi;
}
