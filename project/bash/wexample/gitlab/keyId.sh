#!/usr/bin/env bash

gitlabKeyIdArgs() {
  _ARGUMENTS=(
    [0]='key k "Deployment key" true'
  )
}

gitlabKeyId() {
  # Get lis of enabled keys
  local REPO_KEYS_ALL_JSON=$(wex wexample::gitlab/get -p="deploy_keys")
  local IDS=($(wex json/find -k=id -j="${REPO_KEYS_ALL_JSON}"))
  local KEYS=$(wex json/find -k=key -j="${REPO_KEYS_ALL_JSON}")
  local KEY_LENGTH=${#KEY}
  local COUNT=0

  while read -r LINE; do
    CUT=$(echo ${LINE} | head -c${KEY_LENGTH})
    # Key found.
    if [ "${CUT}" == "${KEY}" ];then
      # Print id.
      echo ${IDS[${COUNT}]}
      return
    fi

    ((COUNT++))
  done <<< "${KEYS}"
}