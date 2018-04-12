#!/usr/bin/env bash

siteExecArgs() {
  _ARGUMENTS=(
    [0]='container n "Container name suffix like site_name_suffix. Default is web" false'
    [1]='command c "Bash command to execute" true'
  )
}

siteExec() {
  # Expected config file.
  wex site/configWrite -nr

  . ${WEX_WEXAMPLE_SITE_CONFIG}

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

  docker exec ${SITE_NAME}_${CONTAINER} /bin/bash -c "${COMMAND}"

  # Stop website.
  if [[ ${STARTED} == true ]];then
    wex site/stop
  fi;
}
