#!/usr/bin/env bash

portRangeGenerate() {
  local OUTPUT=''
  local FINAL_SITE_PORT_RANGE=0
  local FINAL_SITE_PORT_RANGE_FOUND=false
  local SITES_PATHS=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  # Ports
  for RANGE in $(seq 0 9); do
    # Port range still not found
    if [ "${FINAL_SITE_PORT_RANGE_FOUND}" == false ];then
      USED=false

      # Search into all sites
      for SITE_PATH in ${SITES_PATHS[@]}
      do
         # Config file exists
         if [ -f ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG} ];then
          # Load config
          . ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}
          if [ "${STARTED}" == true ] && [ ${SITE_PORT_RANGE} == ${FINAL_SITE_PORT_RANGE} ];then
            USED=true
          fi
        fi
      done

      if [ "${USED}" == false ];then
        # Port range found
        FINAL_SITE_PORT_RANGE_FOUND=true
      else
        # Search next one.
        ((FINAL_SITE_PORT_RANGE++))
      fi
    fi
  done;

  echo 7${FINAL_SITE_PORT_RANGE}
}