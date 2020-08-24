#!/usr/bin/env bash

siteLogsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteLogs() {
  . ${WEX_APP_CONFIG}

  # Use default container if missing
  docker logs $(wex site/container -c=${CONTAINER_NAME}) -f
}
