#!/usr/bin/env bash

serverStartArgs() {
  _ARGUMENTS=(
    [0]='no_recreate n "Do not recompose if already running" false'
    [1]='port p "Port for accessing sites" false'
  )
}

serverStart() {
  # Check if running.
  if [ ! -z ${NO_RECREATE+x} ] && [[ $(wex server/started) == true ]]; then
    return;
  fi

  if [ ! -d ${WEX_WEXAMPLE_DIR_PROXY} ];then
    sudo mkdir -p ${WEX_WEXAMPLE_DIR_PROXY}
  fi

  cd ${WEX_WEXAMPLE_DIR_PROXY}

  sudo mkdir -p ${WEX_WEXAMPLE_DIR_PROXY}tmp
  sudo touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
  sudo touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites

  if [ "${PORT}" == "" ];then
    local PORT=$([[ "$(uname -s)" == Darwin ]] && echo 4242 || echo 80)
  fi

  # TODO Check if a process is using port 80 (or given port)
  #   netstat -tulpn | grep :80

  export WEX_SERVER_PORT_PUBLIC=${PORT}

  if [ ! -f ${WEX_WEXAMPLE_DIR_PROXY}.wex ];then
    # -E to keep port global variable to use in config build.
    sudo -E wex site/init -s=proxy -n=wex_server -e=prod --git=false
  fi

  wex site/start

  # Wait starting.
  _wexMessage "Waiting server starts..."
  sleep 5
}
