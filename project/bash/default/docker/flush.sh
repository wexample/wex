#!/usr/bin/env bash

dockerFlush() {
  local BOOL=$(wex prompt/yn -q="It will remove all containers / images / networks, are you sure ? Type n to stop :")

  if [ "${BOOL}" = false ];then
    return
  fi

  wex docker/stopAll

  _wexLog "Flushing images"
  local IMAGES
  IMAGES=$(docker images -qa);
  if [ "${IMAGES}" != "" ];then
    # Remove all images
    docker rmi "${IMAGES}" -f
  fi

  _wexLog "Flushing networks"
  local NETWORKS
  NETWORKS=$(docker network ls -q --filter type=custom);
  if [ "${NETWORKS}" != "" ];then
    # Remove all networks
    docker network rm "${NETWORKS}"
  fi
}
