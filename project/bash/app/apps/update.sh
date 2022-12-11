#!/usr/bin/env bash

appsUpdateArgs() {
  _AS_NON_SUDO=false
}

appsUpdate() {
  # Load sites list
  local SITES_PATHS=($(cat ${WEX_PROXY_APPS_REGISTRY}))
  local DIR_CURRENT=$(realpath ./)
  # Rebuild sites list.
  local SITES_PATHS_FILTERED=()
  local SITES_FILE=""

  if [ "$(wex proxy/started)" = true ];then
    for SITE_PATH in ${SITES_PATHS[@]}
    do
      local EXISTS=false
      local CONFIG=${SITE_PATH}${WEX_APP_CONFIG}

      # Config must exist.
      if [ -f ${CONFIG} ];then
        # Prevent duplicates
        for SITE_SEARCH in ${SITES_PATHS_FILTERED[@]}
        do
          if [ "${SITE_SEARCH}" = "${SITE_PATH}" ];then
            EXISTS=true
          fi
        done;

        # Load config.
        . "${CONFIG}"

        if [ "${EXISTS}" = false ] && [ "${STARTED}" = true ];then
          cd "${SITE_PATH}"
          if [ "$(wex app/started)" = true ];then
            SITES_PATHS_FILTERED+=(${SITE_PATH})
            SITES_FILE+="\n"${SITE_PATH}
          fi
        fi
      fi
    done
  fi

  cd "${DIR_CURRENT}"

  # Store sites list.
  echo -e "${SITES_FILE}" | tee "${WEX_PROXY_APPS_REGISTRY}" > /dev/null
}
