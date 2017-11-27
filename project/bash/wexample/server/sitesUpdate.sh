#!/usr/bin/env bash

serverSitesUpdate() {

  # Load sites list
  SITES_PATHS=($(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites))
  # Rebuild sites list.
  SITES_PATHS_FILTERED=()

  SITES_FILE=""
  SITES=()
  for SITE_PATH in ${SITES_PATHS[@]}
  do
    EXISTS=false

    # Prevent duplicates
    for SITE_SEARCH in ${SITES_PATHS_FILTERED[@]}
    do
      if [[ ${SITE_SEARCH} == ${SITE_PATH} ]];then
        EXISTS=true
      fi
    done;

    if [[ ${EXISTS} == false ]];then
      SITES_PATHS_FILTERED+=(${SITE_PATH})
      SITES_FILE+="\n"${SITE_PATH}
    fi
  done

  # Store sites list.
  echo -e ${SITES_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
}
