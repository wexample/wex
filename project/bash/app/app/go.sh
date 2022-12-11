#!/usr/bin/env bash

appGoArgs() {
  _ARGUMENTS=(
    'container_name c "Container name suffix like site_name_suffix. Default is web" false'
    'super_user su "Run as sudo inside container" false'
  )
}

appGo() {
  # Use default container if missing
  local CONTAINER
  local COMMAND

  CONTAINER=$(wex app/container -c="${CONTAINER_NAME}")
  COMMAND=$(wex hook/exec -c=appGo --quiet)
  
  if [ "${COMMAND}" != '' ];then
    COMMAND+=' &&  /bin/bash'
  fi

  if [ "${SUPER_USER}" = "true" ];then
    ARGS+=" -u 0 "
  fi

  # docker attach
  docker exec -it ${ARGS} "${CONTAINER}" /bin/bash -c "${COMMAND}"
}
