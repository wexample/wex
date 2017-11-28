#!/usr/bin/env bash

siteLogsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteLogs() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Default container name.
  if [ -z ${CONTAINER+x} ]; then
    CONTAINER=web
  fi

  docker logs ${SITE_NAME}_${CONTAINER}
}
