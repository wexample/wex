#!/usr/bin/env bash

# TODO not tested
sitesStart() {
  local PATH_SITES=/var/www/
  local SITES=$(ls ${PATH_SITES})

  for SITE in ${SITES[@]}
  do

    if [ ! -d ${DIR} ];then
      return;
    fi

    local PATH=${PATH_SITES}${SITE}
    local SITE_ENVS=$(/bin/ls ${PATH})

    for SITE_ENV in ${SITE_ENVS[@]}
    do
      local PATH="${PATH}/${SITE_ENV}"
      if [ -d ${PATH} ];then
        cd ${PATH}
        wex site/start
      fi;
    done
  done
}

