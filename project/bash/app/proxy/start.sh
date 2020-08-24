#!/usr/bin/env bash

proxyStartArgs() {
  _ARGUMENTS=(
    'no_recreate n "Do not recompose if already running" false'
    'port p "Port for accessing sites" false'
  )
  _AS_NON_SUDO=false
}

proxyStart() {
  # Check if running.
  if [ ! -z ${NO_RECREATE+x} ] && [ "$(wex proxy/started)" = true ]; then
    return;
  fi

  wex var/set -n=PROXY_ERROR -v=false

  if [ ! -d "${WEX_WEXAMPLE_DIR_PROXY}" ];then
    mkdir -p "${WEX_WEXAMPLE_DIR_PROXY}"
  fi

  chmod -R 777 "${WEX_WEXAMPLE_DIR_PROXY}"

  cd "${WEX_WEXAMPLE_DIR_PROXY}" || return

  mkdir -p "${WEX_WEXAMPLE_DIR_PROXY}tmp"
  touch "${WEX_DIR_PROXY_TMP}hosts"
  touch "${WEX_PROXY_APPS_REGISTRY}"

  if [ "${PORT}" = "" ];then
    local PORT
    # For macos, use 4242 as default port.
    PORT=$([[ "$(uname -s)" == Darwin ]] && echo 4242 || echo 80)
  fi

  # Check if a process is using port 80 (or given port)
  local PROCESSES
  PROCESSES=$(netstat -tulpn | grep ":${PORT}")

  if [ "${PROCESSES}" != "" ];then
    _wexError "A process is already running on port ${PORT}"
    echo "${PROCESSES}"

    wex var/set -n=PROXY_ERROR -v=ERR_PORT_NOT_AVAILABLE
    return
  fi

  export WEX_SERVER_PORT_PUBLIC=${PORT}

  if [ ! -f "${WEX_WEXAMPLE_DIR_PROXY}.wex" ];then
    # -E to keep port global variable to use in config build.
    sudo -E wex app::app/init -s=proxy -n=wex_server -e=prod --git=false
  fi

  _wexLog "Starting proxy app"
  wex app/start

  # Wait starting.
  _wexLog "Waiting proxy starts..."
  sleep 5
}
