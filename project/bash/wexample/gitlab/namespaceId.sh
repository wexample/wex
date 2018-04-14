#!/usr/bin/env bash

gitlabNamespaceIdArgs() {
  _ARGUMENTS=(
    [0]='group g "Group name" true'
  )
}

gitlabNamespaceId() {
  # Find id
  local ID=$(wex wexample::gitlab/get -p=namespaces -qs="search="${GROUP} -k=id)
  # Is number ?
  if [[ $(wex var/isNumber -v=${ID}) == true ]]; then
    echo ${ID}
  else
    echo false
  fi
}
