#!/usr/bin/env bash

serverInfo() {
  # TODO use server/sites
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(wex text/trim -t=${SITE_PATH}) != "" ]];then
      #SPLIT=($(wex text/split -s="=" -t=${SITE}))
      #echo ${SPLIT[0]}
      echo -e "  Path : \t"${SITE_PATH}
    fi
  done;
}
