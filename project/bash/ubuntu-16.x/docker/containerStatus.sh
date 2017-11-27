#!/usr/bin/env bash

dockerContainerStatus() {
  CONTAINERS=($(docker ps -aq))

  for CONTAINER in ${CONTAINERS[@]}
  do
    #echo "  "${CONTAINER}
    docker info d${CONTAINER}
  done;
}
