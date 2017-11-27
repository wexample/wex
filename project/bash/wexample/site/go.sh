#!/usr/bin/env bash

siteGoArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteGo() {
  SITE_NAME=$(wex site/config -k=name)

  # Default container name.
  if [ -z ${CONTAINER+x} ]; then
    CONTAINER=web
  fi

  docker attach ${SITE_NAME}_${CONTAINER}
}
