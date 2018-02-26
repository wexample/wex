#!/usr/bin/env bash

sitesStop() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(wex text/trim -t=${SITE_PATH}) != "" ]];then
      cd ${SITE_PATH}
      wex site/stop
    fi
  done;
}
