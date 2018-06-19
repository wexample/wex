#!/usr/bin/env bash

containersStart() {
  CONTAINERS=$(wex containers/list)
  # Start all
  for CONTAINER in ${CONTAINERS[@]}
  do
    docker start ${CONTAINER}
  done;
}
