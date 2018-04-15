#!/usr/bin/env bash

gitlabNamespaceIdArgs() {
  _ARGUMENTS=(
    [0]='group g "Group name" true'
  )
}

gitlabNamespaceId() {
  # Get json response
  local JSON=$(wex wexample::gitlab/get -p=namespaces -qs="search="${GROUP})
  # Find id
  local ID=$(echo -e "${JSON}" | sed -E 's/.*id":(.*),"name":"'${GROUP}'".*$/\1/')
  # Is number ?
  if [[ $(wex var/isNumber -v=${ID}) == true ]]; then
    echo ${ID}
  else
    echo false
  fi
}
