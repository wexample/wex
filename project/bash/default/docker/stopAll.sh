#!/usr/bin/env bash

dockerStopAll() {
  _wexLog "Stopping containers"
  # Containers
  local CONTAINERS=($(docker ps -qa))
  if [ ${#CONTAINERS[@]} -gt 0 ];then
    # Stop all
    docker stop "${CONTAINERS[@]}"
    # Remove
    docker rm "${CONTAINERS[@]}" -f
  fi;

  # Networks
  _wexLog "Stopping networks"
  # List all networks except builtin
  local NETWORKS=($(docker network ls -q --filter type=custom))
  if [ ${#CONTAINERS[@]} -gt 0 ];then
    # Remove networks
    docker network rm "${NETWORKS[@]}"
  fi;

  # Volumes
  local VOLUMES;
  _wexLog "Stopping volumes"
  VOLUMES=$(docker volume ls -q)
  if [ ${#CONTAINERS[@]} -gt 1 ];then
    docker volume rm "${VOLUMES[@]}"
  fi;
}
