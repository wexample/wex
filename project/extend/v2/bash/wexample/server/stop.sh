#!/usr/bin/env bash

serverStop() {
  # Stop all sites
  if [ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}apps ];then
    wex wexample::sites/stop
  fi

  # Remove temp files
  sudo rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}config
  sudo rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}apps
  sudo rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
