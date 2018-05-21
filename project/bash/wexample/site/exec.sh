#!/usr/bin/env bash

siteExecArgs() {
  _ARGUMENTS=(
    [0]='container_name n "Container name suffix like site_name_suffix. Default is web" false'
    [1]='command c "Bash command to execute" true'
  )
}

siteExec() {
  # Expected config file.
  wex config/write -nr

  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Use default container if missing
  local CONTAINER=$(wex site/container -c=${CONTAINER_NAME})

  # Save if we had to start website manually
  # we will stop it at end.
  local STARTED_LOCALLY=false

  # Start website.
  if [[ $(wex site/started) == false ]];then
    STARTED_LOCALLY=true
    wex site/start
  fi;

  docker exec -ti ${CONTAINER} /bin/bash -c "${COMMAND}"

  # Stop website.
  if [[ ${STARTED_LOCALLY} == true ]];then
    wex site/stop
  fi;
}
