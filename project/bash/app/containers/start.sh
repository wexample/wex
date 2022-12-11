#!/usr/bin/env bash

containersStart() {
  local CONTAINERS
  CONTAINERS=$(wex containers/list)
  # Start all
  for CONTAINER in ${CONTAINERS[@]}
  do
    docker start "${CONTAINER}"
  done;
}
