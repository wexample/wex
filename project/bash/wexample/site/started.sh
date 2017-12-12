#!/usr/bin/env bash

siteStartedArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

siteStarted() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Config file exists
  if [[ -f ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG} ]];then
    # Load config
    . ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG}
    # Started && into server
    if [ ${STARTED} == true ] && [[ $(wex server/started) == true ]] && [[ $(wex file/lineExists -f=${WEX_WEXAMPLE_DIR_PROXY_TMP}sites -l=$(realpath ${DIR_SITE})"/") == true ]];then
        echo true
        return
    fi

    echo $([ ${STARTED} == true ] && echo true || echo false)
    return
  fi

  echo false
}
