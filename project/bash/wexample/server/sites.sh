#!/usr/bin/env bash

serverSites() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  SITES=()

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(wex text/trim -t=${SITE_PATH}) != "" ]];then
      EXISTS=false
      # Prevent duplicates
      for SITE_SEARCH in ${SITES[@]}
      do
        if [[ ${SITE_SEARCH} == ${SITE_PATH} ]];then
          EXISTS=true
        fi
      done;

      if [[ ${EXISTS} == false ]] && [[ $(wex site/started -d=${SITE_PATH}) == true ]];then
        wex site/configLoad -d=${SITE_PATH}
        SITES+=(${SITE_NAME})
      fi
    fi
  done;

  echo ${SITES[@]}
}
