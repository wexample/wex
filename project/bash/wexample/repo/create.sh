#!/usr/bin/env bash

repoCreateArgs() {
  _ARGUMENTS=(
    [0]='name n "Repo name" false'
    [1]='namespace ns "Namespace" false'
  )
}

repoCreate() {
  # Get repo namespace
  local REPO_NAMESPACE=$(wex repo/namespace)
  local REPO_NAMESPACE_ID=''
  local NAMESPACE_ID=$(wex wexample::gitlab/namespaceId -g=${REPO_NAMESPACE})
  # Load site name.
  wex config/load
  # Create.
  OUTPUT=$(wex wexample::gitlab/post -p="projects" -d="path="${SITE_NAME}"&namespace_id="${NAMESPACE_ID})

  echo ${OUTPUT}
}
