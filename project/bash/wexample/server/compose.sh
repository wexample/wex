#!/usr/bin/env bash

serverComposeArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" true'
  )
}

serverCompose() {
  # Load config
  . ${WEX_WEXAMPLE_DIR_PROXY_TMP}config

  # Export variables
  export WEX_DOCKER_MACHINE_IP=${WEX_DOCKER_MACHINE_IP}
  export WEX_WEXAMPLE_DIR_TMP=${WEX_WEXAMPLE_DIR_TMP}

  docker-compose -f ${WEX_DIR_ROOT}docker/containers/reverseProxy/docker-compose.yml ${COMMAND}
}
