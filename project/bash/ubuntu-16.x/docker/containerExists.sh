#!/usr/bin/env bash

dockerContainerExistsArgs() {
  _ARGUMENTS=(
    [0]='container c "Container name" true'
  )
}

dockerContainerExists() {
  wex docker/containerRuns -a -c=${CONTAINER}
}
