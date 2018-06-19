#!/usr/bin/env bash

dockerContainerStatus() {
  CONTAINERS=($(docker ps -aq))

  for CONTAINER in ${CONTAINERS[@]}
  do
    docker info ${CONTAINER}
  done;
}
