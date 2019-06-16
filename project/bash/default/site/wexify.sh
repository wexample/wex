#!/usr/bin/env bash

siteWexifyArgs() {
  # Arguments should be compatible wit wex site/init
  _ARGUMENTS=(
    [0]='services s "Services to install" true',
  )
}

siteWexify() {

  # Split services
  local SERVICES_JOINED=$(wex wexample::service/tree -s="${SERVICES}")
  local SERVICES=$(echo ${SERVICES_JOINED} | tr "," "\n")

  # Check services exists
  for SERVICE in ${SERVICES[@]}
  do
    if [ ! -d ${WEX_DIR_DOCKER_SERVICES}${SERVICE} ];then
      # Run per service script
      wex wexample::service/exec -s=${SERVICE} -sf -c=wexify
    fi
  done

  # Init website
  wex site/init ${WEX_ARGUMENTS}
}
