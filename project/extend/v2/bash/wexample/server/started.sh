#!/usr/bin/env bash

serverExecArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Do not use cached result in memory" false'
  )
}

serverStarted() {
  # Performance optimization.
  if [ "${CLEAR_CACHE}" == true ] || [ -z "${WEX_CACHE_WEXAMPLE_SERVER_STARTED+x}" ];then

    if [[ $(wex docker/containerRuns -c=${WEX_WEXAMPLE_PROXY_CONTAINER}) == true ]] &&
      # Config files exists.
      [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}config ]] &&
      [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts ]] &&
      [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}apps ]];then
      WEX_CACHE_WEXAMPLE_SERVER_STARTED=true
    else
      WEX_CACHE_WEXAMPLE_SERVER_STARTED=false
    fi
  fi

  echo ${WEX_CACHE_WEXAMPLE_SERVER_STARTED}
}
