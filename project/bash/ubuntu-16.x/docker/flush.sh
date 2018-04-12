#!/usr/bin/env bash

dockerFlush() {

  # Warn user.
  read -p "It will remove all containers / images / networks, are you sure ? Type n to stop : " ANSWER
  if [ ${ANSWER} == "n" ];then
    return
  fi;

  wex docker/stopAll
  # Remove all images
  docker rmi $(docker images -qa) -f
  # Remove all networks
  docker network rm $(docker network list -q)
}
