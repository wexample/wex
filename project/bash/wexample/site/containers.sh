#!/usr/bin/env bash

siteContainers() {
  CONFIG_YML=$(wex site/configYml)
  SEARCH_VAR="container_name"
  CONTAINERS=()

  for COMPOSE_VAR in ${CONFIG_YML[@]}
  do
    CONTAINER_NAME=$(sed -n "s/^services_\(.*\)_\?${SEARCH_VAR}\=\"\?\(.*\)\"\$/\2/p" <<< ${COMPOSE_VAR})
    if [[ ${CONTAINER_NAME} ]];then
      CONTAINERS+=(${CONTAINER_NAME})
    fi
  done;

  echo ${CONTAINERS[@]}
}
