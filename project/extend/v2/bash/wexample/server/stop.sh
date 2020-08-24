#!/usr/bin/env bash

serverStop() {
  # Stop all sites
  if [ -f ${WEX_PROXY_APPS_REGISTRY} ];then
    wex wexample::sites/stop
  fi

  # Remove temp files
  sudo rm -f ${WEX_DIR_PROXY_TMP}config
  sudo rm -f ${WEX_PROXY_APPS_REGISTRY}
  sudo rm -f ${WEX_DIR_PROXY_TMP}hosts
}
