#!/usr/bin/env bash

sitesListArgs() {
  _ARGUMENTS=(
    [0]='all a "Remove raw list without testing activity" false',
  )
}

# Return actively running sites list.
sitesList() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  SITES=()

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Trim
    SITE_PATH=$(echo -e "${SITE_PATH}" | sed -e 's/^[[:space:]]\{0,\}//' -e 's/[[:space:]]\{0,\}$//')
    # Avoid blank lines.
    if [[ ${SITE_PATH} != "" ]];then
      EXISTS=false

      if [ "${ALL}" != '' ];then
        SITES+=($(basename ${SITE_PATH}))
      else
        # Prevent duplicates
        for SITE_SEARCH in ${SITES[@]}
        do
          if [[ ${SITE_SEARCH} == ${SITE_PATH} ]];then
            EXISTS=true
          fi
        done;

        if [ ${EXISTS} == false ] && [ $(wex site/started -d=${SITE_PATH}) == true ];then
          . ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}
          SITES+=(${SITE_NAME})
        fi
      fi
    fi
  done;

  echo ${SITES[@]}
}
