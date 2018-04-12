#!/usr/bin/env bash

dockerStopAll() {
  # Containers
  CONTAINERS=($(docker ps -qa))
  if (( ${#CONTAINERS[@]} > 0 ));then
    # Stop all
    docker stop ${CONTAINERS[@]}
    # Remove
    docker rm ${CONTAINERS[@]} -f
  fi;

  # Networks
  # List all networks except builtin
  NETWORKS=($(docker network ls -q --filter type=custom))
  if (( ${#NETWORKS[@]} > 0 ));then
    # Remove networks
    docker network rm ${NETWORKS[@]}
  fi;
}
