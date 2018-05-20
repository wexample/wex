#!/usr/bin/env bash

siteGoArgs() {
  _ARGUMENTS=(
    [0]='container_name c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteGo() {
  # Use default container if missing
  local CONTAINER=$(wex site/container -c=${CONTAINER_NAME})
  # docker attach
  docker exec -it ${CONTAINER} /bin/sh
}
