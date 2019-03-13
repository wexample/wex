#!/usr/bin/env bash

siteExecArgs() {
  _ARGUMENTS=(
    [0]='container_name n "Container name suffix like site_name_suffix. Default is web" false'
    [1]='command c "Bash command to execute" true'
    [2]='starts "Start container verification" false'
    [3]='localized l "Execute script in project location (it may be the default behavior in the future)" false'
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
  if [ "${STARTS}" == true ] && [ $(wex site/started) == false ];then
    STARTED_LOCALLY=true
    wex site/start
  fi;

  if [ "${LOCALIZED}" == true ];then
    COMMAND="$(wex service/exec -c=go) && ${COMMAND}"
  fi;

  docker exec -ti ${CONTAINER} /bin/bash -c "${COMMAND}"

  # Stop website.
  if [ "${STARTS}" == true ] && [ ${STARTED_LOCALLY} == true ];then
    wex site/stop
  fi;
}
