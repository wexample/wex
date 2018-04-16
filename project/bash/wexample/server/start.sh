#!/usr/bin/env bash

serverStartArgs() {
  _ARGUMENTS=(
    [0]='no_recreate n "Do not recompose if already running" false'
  )
}

serverStart() {
  # Check if running.
  if [ ! -z ${NO_RECREATE+x} ] && [[ $(wex server/started) == true ]]; then
    return;
  fi

  # Create temp dit if not exists.
  mkdir -p ${WEX_WEXAMPLE_DIR_PROXY_TMP}

  # Create config file
  PROXY_CONFIG_FILE+="\nWEX_DOCKER_MACHINE_IP="$(wex docker/ip)
  PROXY_CONFIG_FILE+="\nWEX_IMAGES_VERSION="$(wex wex/version)
  # Save param file.
  echo -e ${PROXY_CONFIG_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}config
  touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
  touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites

  # Recompose
  wex wexample::server/compose -c="up -d --build"
}
