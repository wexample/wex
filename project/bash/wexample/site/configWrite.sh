#!/usr/bin/env bash

siteConfigWrite() {

  # Create temp dirs if not exists.
  mkdir -p ${WEX_WEXAMPLE_DIR_TMP}
  mkdir -p ${WEX_WEXAMPLE_SITE_DIR_TMP}

  # Get site name.
  SITE_NAME=$(wex site/config -k=name)
  SITE_CONFIG_FILE=""
  SITE_PATH=$(realpath ./)"/"
  SITE_CONFIG_FILE+="\nSITE_NAME="${SITE_NAME}

  SITES_PATHS=${SITES_PATHS_FILTERED}
  FINAL_SITE_PORT_RANGE=0
  FINAL_SITE_PORT_RANGE_FOUND=false

  # Ports
  for RANGE in $(seq 0 9); do
    # Port range still not found
    if [[ ${FINAL_SITE_PORT_RANGE_FOUND} == false ]];then
      USED=false

      # Search into all sites
      for SITE_PATH in ${SITES_PATHS_FILTERED[@]}
      do
        # Config file exists
        if [[ -f ${SITE_PATH}"tmp/config" ]];then
          # Load config
          . ${SITE_PATH}"tmp/config"
          if [[ ${SITE_PORT_RANGE} == ${FINAL_SITE_PORT_RANGE} ]];then
            USED=true
          fi
        fi
      done

      if [[ ${USED} == false ]];then
        # Port range found
        FINAL_SITE_PORT_RANGE_FOUND=true
      else
        # Search next one.
        ((FINAL_SITE_PORT_RANGE++))
      fi
    fi
  done;

  # Save in config.
  SITE_CONFIG_FILE+="\nSITE_PORT_RANGE="${FINAL_SITE_PORT_RANGE}

  FINAL_SITE_PORT_RANGE_STOP=100
  LOCAL_COUNTER=10
  LOCAL_COUNTER_VAR=0
  while [ ${LOCAL_COUNTER} -lt ${FINAL_SITE_PORT_RANGE_STOP} ]; do
    VAR_NAME="WEX_COMPOSE_PORT_"${LOCAL_COUNTER_VAR}
    # Use a common range.
    PORT=8${FINAL_SITE_PORT_RANGE}${LOCAL_COUNTER}
    # One Up
    ((LOCAL_COUNTER++))
    ((LOCAL_COUNTER_VAR++))
    # Add to registry.
    SITE_CONFIG_FILE+="\n"${VAR_NAME}"="${PORT}
  done

  # Save param file.
  echo -e ${SITE_CONFIG_FILE} > ${WEX_WEXAMPLE_SITE_DIR_TMP}config

  # Create docker-compose.build.yml
  wex site/compose -c="config" > ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}

}
