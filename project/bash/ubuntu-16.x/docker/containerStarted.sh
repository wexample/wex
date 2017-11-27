#!/usr/bin/env bash

dockerContainerStartedArgs() {
  _ARGUMENTS=(
    [0]='names n "Names of containers separated by a comma. Return true only if one container is started." true',
  )
}

dockerContainerStarted() {
  RUNNING=$(docker ps -q)
  NAMES=$(wex text/split -t=${NAMES} -s=",")

  # Inspect stopped containers
  for CONTAINER_ID in ${RUNNING[@]}
  do
    CONTAINER_NAME=$(wex docker/containerName -i=${CONTAINER_ID})
    # Allow several names.
    for NAME in ${NAMES[@]}
    do
      # One container is running.
      if [[ ${CONTAINER_NAME} == ${NAME} ]];then
        echo true
        return
      fi
    done;
  done;

  echo false
}
