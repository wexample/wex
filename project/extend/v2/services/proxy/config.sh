#!/usr/bin/env bash

proxyConfig() {

  export WEX_DOCKER_MACHINE_IP=$(wex docker/ip)
  export WEX_WEXAMPLE_DIR_TMP=${WEX_WEXAMPLE_DIR_TMP}
  export WEX_IMAGES_VERSION=$(wex wex/version)
  # MacOs Does not support access on port 80
  export SERVER_PORT_PUBLIC=$([[ "$(uname -s)" == Darwin ]] && echo 4242 || echo 80)

  local CONFIG=''
  CONFIG+="\nWEX_DOCKER_MACHINE_IP="${WEX_DOCKER_MACHINE_IP}
  CONFIG+="\nWEX_WEXAMPLE_DIR_TMP="${WEX_WEXAMPLE_DIR_TMP}
  CONFIG+="\nWEX_IMAGES_VERSION="${WEX_IMAGES_VERSION}
  CONFIG+="\nSERVER_PORT_PUBLIC="${SERVER_PORT_PUBLIC}

  echo ${CONFIG}
}
