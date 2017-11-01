#!/usr/bin/env bash

dockerContainerRunsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name" true'
  )
}

dockerContainerRuns() {
  if [[ "$(docker ps | grep ${CONTAINER})" ]]; then
    echo true
  else
    echo false
  fi;
}
