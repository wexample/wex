#!/usr/bin/env bash

siteContainersArgs() {
  _ARGUMENTS=(
    [0]='remove_prefix rm "Remove the name of the site from container name" false',
    [1]='file_compose f "Docker compose file" false',
  )
}

siteContainers() {
  CONFIG_YML=$(wex site/configYml -f=${FILE_COMPOSE})
  SEARCH_VAR="container_name"
  CONTAINERS=()

  # Remove prefix
  if [ "${REMOVE_PREFIX}" == true ];then
    . ${WEX_WEXAMPLE_SITE_CONFIG}
    REGEX="s/^services_\(.*\)_\?${SEARCH_VAR}\=\"${SITE_NAME}_\(.*\)\"\$/\2/p"
  else
    REGEX="s/^services_\(.*\)_\?${SEARCH_VAR}\=\"\?\(.*\)\"\$/\2/p"
  fi

  for COMPOSE_VAR in ${CONFIG_YML[@]}
  do
    CONTAINER_NAME=$(sed -n ${REGEX} <<< ${COMPOSE_VAR})
    if [[ ${CONTAINER_NAME} ]];then
      CONTAINERS+=(${CONTAINER_NAME})
    fi
  done;

  echo ${CONTAINERS[@]}
}
