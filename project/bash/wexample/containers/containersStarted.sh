#!/usr/bin/env bash

containersStartedArgs() {
  _ARGUMENTS=(
    [0]='all a "All containers runs" false',
  )
}

containersStarted() {
  # Get site name.
  CONTAINERS=$(wex containers/list)
  # If empty stop here.
  if [ "${CONTAINERS}" == "" ];then
    # No service, we consider that everything runs.
    echo true
    return
  fi
  CONTAINERS=$(wex array/join -a="${CONTAINERS}" -s=",")
  # Expect all containers runs.
  wex docker/containerStarted -n="${CONTAINERS}" -a=${ALL}
}
