#!/usr/bin/env bash

serverInfo() {
  REGISTRY=$(cat ${WEX_PROXY_APPS_REGISTRY})

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(wex text/trim -t=${SITE_PATH}) != "" ]];then
      echo -e "  Path : \t"${SITE_PATH}
    fi
  done;

  cat ${WEX_DIR_PROXY_TMP}config
}
