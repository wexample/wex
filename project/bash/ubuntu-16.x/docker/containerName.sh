#!/usr/bin/env bash

dockerContainerNameArgs() {
  _ARGUMENTS=(
    [0]='id i "Id of container" true',
  )
}

dockerContainerName() {
  NAME=$(docker inspect --format="{{.Name}}" ${ID})
  # Remove first char slash.
  echo ${NAME:1}
}
