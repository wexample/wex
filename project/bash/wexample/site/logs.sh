#!/usr/bin/env bash

siteLogsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteLogs() {
  SITE_NAME=$(wex site/config -k=name)

  # Default container name.
  if [ -z ${CONTAINER+x} ]; then
    CONTAINER=web
  fi

  docker logs ${SITE_NAME}_${CONTAINER}
}
