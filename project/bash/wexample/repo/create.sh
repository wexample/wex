#!/usr/bin/env bash

repoCreateArgs() {
  _ARGUMENTS=(
    [0]='name n "Repo name" false'
    [1]='namespace ns "Namespace" false'
  )
}

repoCreate() {
  local NAMESPACE_ID=''
  if [ ! -z "${NAMESPACE+x}" ]; then
    NAMESPACE_ID=$(wex wexample::gitlab/namespaceId -g=${NAMESPACE})
  fi;

  wex wexample::gitlab/post -p="projects" -d="path="${NAME}"&namespace_id="${NAMESPACE_ID}
}
