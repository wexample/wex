#!/usr/bin/env bash

containerRebuildArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name" true'
  )
}

containerRebuild() {
  . ${WEX_APP_CONFIG}

  local CONTAINER=$(wex site/container -c=${CONTAINER})

  docker stop ${CONTAINER}

  docker-compose -f tmp/docker-compose.build.yml up -d ${CONTAINER}
}