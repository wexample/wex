#!/usr/bin/env bash

sitesStop() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(${WEX_DIR_V3_CMD} string/trim -s=${SITE_PATH}) != "" ]];then
      # Keep wex_server alive.
      if [ $(basename ${SITE_PATH}) != 'wex_server' ];then
        cd ${SITE_PATH}
        wex site/stop
      fi
    fi
  done;
}
