#!/usr/bin/env bash

dockerFlush() {
  wexample dockerStop
  # Remove all images
  docker rmi $(docker images -qa)
  # Remove all networks
  docker network rm $(docker network list -q);
}
