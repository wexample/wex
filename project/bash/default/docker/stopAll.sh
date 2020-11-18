#!/usr/bin/env bash

dockerStopAll() {
  # Containers
  local CONTAINERS=($(docker ps -qa))
  if [ ${#CONTAINERS[@]} -gt 0 ];then
    # Stop all
    docker stop "${CONTAINERS[@]}"
    # Remove
    docker rm "${CONTAINERS[@]}" -f
  fi;

  # Networks
  # List all networks except builtin
  local NETWORKS=($(docker network ls -q --filter type=custom))
  if [ ${#CONTAINERS[@]} -gt 0 ];then
    # Remove networks
    docker network rm "${NETWORKS[@]}"
  fi;

  # Volumes
  local VOLUMES;
  VOLUMES=$(docker volume ls -q)
  if [ ${#CONTAINERS[@]} -gt 1 ];then
    docker volume rm "${VOLUMES[@]}"
  fi;
}
