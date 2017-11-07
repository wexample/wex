#!/usr/bin/env bash

siteExecArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name suffix like site_name_suffix. Default is web" false'
    [1]='command e "Bash command to execute" true'
  )
}

siteExec() {
  SITE_NAME=$(wex site/config -k=name)

  # Default container name.
  if [ -z ${CONTAINER+x} ]; then
    CONTAINER=web
  fi

  # Save if we had to start website manually
  # we will stop it at end.
  STARTED=false

  # Start website.
  if [[ $(wex docker/containerRuns -c=${SITE_NAME}"_web") == false ]];then
    STARTED=true
    wex site/start
  fi;

  docker exec ${SITE_NAME}_${CONTAINER} ${COMMAND}

  # Stop website.
  if [[ ${STARTED} == true ]];then
    wex site/stop
  fi;
}
