#!/usr/bin/env bash

sitesUpdate() {
  # Load sites list
  local SITES_PATHS=($(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites))
  local DIR_CURRENT=$(realpath ./)
  # Rebuild sites list.
  local SITES_PATHS_FILTERED=()
  local SITES_FILE=""
  if [ $(wex server/started) == true ];then
    SITES=()
    for SITE_PATH in ${SITES_PATHS[@]}
    do
      local EXISTS=false
      local CONFIG=${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}

      # Config must exist.
      if [ -f ${CONFIG} ];then
        # Prevent duplicates
        for SITE_SEARCH in ${SITES_PATHS_FILTERED[@]}
        do
          if [ ${SITE_SEARCH} == ${SITE_PATH} ];then
            EXISTS=true
          fi
        done;

        # Load config.
        . ${CONFIG}

        if [ "${EXISTS}" == false ] && [ "${STARTED}" == true ];then
          cd ${SITE_PATH}
          if [ $(wex site/started) == true ];then
            SITES_PATHS_FILTERED+=(${SITE_PATH})
            SITES_FILE+="\n"${SITE_PATH}
          fi
        fi
      fi
    done
  fi

  cd ${DIR_CURRENT}

  # Store sites list.
  echo -e ${SITES_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
}
