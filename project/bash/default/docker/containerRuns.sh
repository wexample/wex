#!/usr/bin/env bash

dockerContainerRunsArgs() {
  _ARGUMENTS=(
    'container c "Container name" true'
    'all a "All, included stopped ones" false'
  )
}

dockerContainerRuns() {
  if [ "${ALL}" = true ];then
    ALL="-a"
  fi

  if docker ps ${ALL} | grep -q "${CONTAINER}"; then
    echo true
  else
    echo false
  fi;
}
