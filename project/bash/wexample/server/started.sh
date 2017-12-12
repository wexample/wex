#!/usr/bin/env bash

serverStarted() {

  if [[ $(wex docker/containerRuns -c=${WEX_WEXAMPLE_PROXY_CONTAINER}) == true ]] &&
    # Config files exists.
    [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}config ]] &&
    [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts ]] &&
    [[ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites ]];then
    echo true
    return
  fi

  echo false
}