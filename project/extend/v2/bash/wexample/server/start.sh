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

  if [ ! -d ${WEX_WEXAMPLE_DIR_PROXY} ];then
    mkdir -p ${WEX_WEXAMPLE_DIR_PROXY}
  fi

  cd ${WEX_WEXAMPLE_DIR_PROXY}

  mkdir -p ${WEX_WEXAMPLE_DIR_PROXY}tmp
  touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
  touch ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites

  if [ ! -f ${WEX_WEXAMPLE_DIR_PROXY}.wex ];then
    wex site/init -s=proxy -n=wex_server -e=prod --git=false
  fi

  wex site/start

  # Wait starting.
  sleep 20
}
