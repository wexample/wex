#!/usr/bin/env bash

appsListArgs() {
  _ARGUMENTS=(
    'all a "Return raw list without testing activity" false',
    'count c "Return only number of sites found" false',
  )
}

# Return actively running sites list.
appsList() {
  local REGISTRY=$(cat ${WEX_PROXY_APPS_REGISTRY})
  local SITES_COUNT=0;
  local SITES=();

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Trim
    SITE_PATH=$(echo -e "${SITE_PATH}" | sed -e 's/^[[:space:]]\{0,\}//' -e 's/[[:space:]]\{0,\}$//')
    # Avoid blank lines.
    if [[ ${SITE_PATH} != "" ]];then
      EXISTS=false

      if [ "${ALL}" != '' ];then
        SITES+=($(basename ${SITE_PATH}))
        ((SITES_COUNT++))
      else
        # Prevent duplicates
        for SITE_SEARCH in ${SITES[@]}
        do
          if [[ ${SITE_SEARCH} == ${SITE_PATH} ]];then
            EXISTS=true
          fi
        done;

        if [ ${EXISTS} == false ] && [ $(wex app/started -d=${SITE_PATH}) == true ];then
          . ${SITE_PATH}${WEX_APP_CONFIG}
          SITES+=(${SITE_NAME})
          ((SITES_COUNT++))
        fi
      fi
    fi
  done;

  if [ "${COUNT}" == "true" ];then
    echo ${SITES_COUNT}
  else
    echo ${SITES[@]}
  fi
}
