#!/usr/bin/env bash

proxyExecArgs() {
  _ARGUMENTS=(
    'clear_cache cc "Do not use cached result in memory" false'
  )
}

proxyStarted() {
  # Performance optimization.
  if [ "${CLEAR_CACHE}" = true ] || [ -z "${WEX_CACHE_PROXY_STARTED+x}" ];then
    if [ "$(wex docker/containerRuns -c="${WEX_PROXY_CONTAINER}")" = true ] &&
      # Config files exists.
      [ -f "${WEX_DIR_PROXY_TMP}config" ] &&
      [ -f "${WEX_DIR_PROXY_TMP}hosts" ] &&
      [ -f "${WEX_PROXY_APPS_REGISTRY}" ];then

      WEX_CACHE_PROXY_STARTED=true
    else
      WEX_CACHE_PROXY_STARTED=false
    fi
  fi

  echo "${WEX_CACHE_PROXY_STARTED}"
}
