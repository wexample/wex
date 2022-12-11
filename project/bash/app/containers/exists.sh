#!/usr/bin/env bash

containersExistsArgs() {
  _ARGUMENTS=(
    'all a "All containers exists" false',
  )
}

containersExists() {
  local EXPECTED=($(wex containers/list))
  local RUNNING=($(docker ps -aq))
  local NAMES=$(wex string/split -t="${NAMES}")
  local ALL_RUNS=true
  local CONTAINER_NAME

  for NAME in ${EXPECTED[@]}
  do
    local EXISTS=false

    # Inspect not stopped containers
    for CONTAINER_ID in ${RUNNING[@]}
    do
      CONTAINER_NAME=$(wex docker/containerName -i="${CONTAINER_ID}")
      # Searched is running.
      if [ "${CONTAINER_NAME}" = "${NAME}" ];then
        EXISTS=true
      fi
    done;

    # Expecting all exists.
    if [ "${ALL}" = true ];then
      if [ "${EXISTS}" = false ];then
        echo false
        return
      fi
      # Or continue
    # Only one can exist
    elif [ "${EXISTS}" = true ];then
      echo true
      return
    fi
  done;

  # All containers should exist,
  # any has been detected as missing.
  if [ "${ALL}" = true ];then
    echo true
    return
  fi

  # One container must run,
  # any has been detected as running.
  echo false
}
