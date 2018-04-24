#!/usr/bin/env bash

containerRebuildArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name" true'
  )
}

containerRebuild() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  CONTAINER=${SITE_NAME}_${CONTAINER}

  docker stop ${CONTAINER}

  docker-compose -f tmp/docker-compose.build.yml up -d ${CONTAINER}
}