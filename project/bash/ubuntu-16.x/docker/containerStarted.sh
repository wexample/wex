#!/usr/bin/env bash

dockerContainerStartedArgs() {
  _ARGUMENTS=(
    [0]='names n "Names of containers separated by a comma. Return true only if one container is started." true',
    [1]='all a "All containers runs" false',
  )
}

dockerContainerStarted() {
  local RUNNING=$(docker ps -q)
  local NAMES=$(wex text/split -t=${NAMES} -s=",")
  local ALL_RUNS=true

  # Allow several names.
  for NAME in ${NAMES[@]}
  do
    local RUNS=false

    # Inspect not stopped containers
    for CONTAINER_ID in ${RUNNING[@]}
    do
      local CONTAINER_NAME=$(wex docker/containerName -i=${CONTAINER_ID})
      # Searched is running.
      if [[ ${CONTAINER_NAME} == ${NAME} ]];then
        RUNS=true
      fi
    done;

    # Expecting all runs.
    if [[ ${ALL} == true ]];then
      if [[ ${RUNS} == false ]];then
        echo false
        return
      fi
    # Only one can run
    elif [[ ${RUNS} == true ]];then
      echo true
      return
    fi
  done;

  # All containers should runs,
  # any has been detected as not running.
  if [[ ${ALL} == true ]];then
    echo true
  # One container must run,
  # any has been detected as running.
  else
    echo false
  fi
}
