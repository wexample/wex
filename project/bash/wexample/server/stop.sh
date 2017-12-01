#!/usr/bin/env bash

serverStop() {
  wex wexample::server/stopSites
  # Decompose
  wex wexample::server/compose -c="down"
  # Remove temp files
  rm ${WEX_WEXAMPLE_DIR_PROXY_TMP}config
  rm ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
  rm ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
