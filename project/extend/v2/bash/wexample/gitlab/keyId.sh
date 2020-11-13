#!/usr/bin/env bash

gitlabKeyIdArgs() {
  _ARGUMENTS=(
    [0]='key k "Deployment key" true'
  )
}

gitlabKeyId() {
  # Get lis of enabled keys
  local REPO_KEYS_ALL_JSON=$(wex wexample::gitlab/get -p="deploy_keys")
  wex json/search -k=id -s=key -v="${KEY}" -j="${REPO_KEYS_ALL_JSON}"
}