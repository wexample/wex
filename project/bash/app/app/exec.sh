#!/usr/bin/env bash

appExecArgs() {
  _DESCRIPTION="Execute a script from inside the container, at project root"
  _ARGUMENTS=(
    'container_name n "Container name suffix like site_name_suffix. Default is web" false'
    'command c "Bash command to execute" true'
    'starts "Start container verification" false'
    'localized l "Execute script in project location" false true'
    'super_user su "Run as sudo inside container" false'
  )
}

appExec() {
  if [ $(wex app/started -ic) = false ];then
    return
  fi

  # Expected config file.
  wex config/write -nr

  . ${WEX_APP_CONFIG}

  # Use default container if missing
  local CONTAINER=$(wex app/container -c=${CONTAINER_NAME})

  # Save if we had to start website manually
  # we will stop it at end.
  local STARTED_LOCALLY=false

  # Start website.
  if [ "${STARTS}" == true ] && [ $(wex app/started) == false ];then
    STARTED_LOCALLY=true
    wex app/start
  fi;

  if [ "${LOCALIZED}" == true ];then
    COMMAND="$(wex service/exec -c=appGo) && ${COMMAND}"
  fi;

  local ARGS=""
  if [ "${NON_INTERACTIVE}" != true ];then
    ARGS+="-ti"
  fi;

  if [ "${SUPER_USER}" = "true" ];then
    ARGS+=" -u 0 "
  fi

  docker exec ${ARGS} "${CONTAINER}" /bin/bash -c "${COMMAND}"

  # Stop website.
  if [ "${STARTS}" == true ] && [ ${STARTED_LOCALLY} == true ];then
    wex app/stop
  fi;
}
