#!/usr/bin/env bash

dockerFlush() {
  wex docker/stopAll
  # Remove all images
  docker rmi $(docker images -qa) -f
  # Remove all networks
  docker network rm $(docker network list -q) -f;
}
