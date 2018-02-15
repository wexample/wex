#!/usr/bin/env bash

siteContainersStart() {
  CONTAINERS=$(wex site/containers)
  # Start all
  for CONTAINER in ${CONTAINERS[@]}
  do
    docker start ${CONTAINER}
  done;
}
