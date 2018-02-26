#!/usr/bin/env bash

dockerContainerRunsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name" true'
    [1]='all a "All, included stopped ones" false'
  )
}

dockerContainerRuns() {
  if [ ${ALL} == true ];then
    ALL="-a"
  fi

  if [[ "$(docker ps ${ALL} | grep ${CONTAINER})" ]]; then
    echo true
  else
    echo false
  fi;
}
