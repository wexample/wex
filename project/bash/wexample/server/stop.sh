#!/usr/bin/env bash

serverStop() {
  # Stop all sites
  if [ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites ];then
    wex wexample::server/stopSites
  fi

  # Stop server containers
  if [ -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}config ];then
    # Decompose
    wex wexample::server/compose -c="down"
  fi

  # Remove temp files
  rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}config
  rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
  rm -f ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
