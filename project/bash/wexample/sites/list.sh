#!/usr/bin/env bash

# Return actively running sites list.
sitesList() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  SITES=()

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Trim
    SITE_PATH=$(echo -e "${SITE_PATH}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    # Avoid blank lines.
    if [[ ${SITE_PATH} != "" ]];then
      EXISTS=false
      # Prevent duplicates
      for SITE_SEARCH in ${SITES[@]}
      do
        if [[ ${SITE_SEARCH} == ${SITE_PATH} ]];then
          EXISTS=true
        fi
      done;

      if [[ ${EXISTS} == false ]] && [[ $(wex site/started -d=${SITE_PATH}) == true ]];then
        . ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}
        SITES+=(${SITE_NAME})
      fi
    fi
  done;

  echo ${SITES[@]}
}
