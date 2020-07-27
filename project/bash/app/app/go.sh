#!/usr/bin/env bash

appGoArgs() {
  _ARGUMENTS=(
    [0]='container_name c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

appGo() {
  # Use default container if missing
  local CONTAINER=$(wex site/container -c=${CONTAINER_NAME})
  local COMMAND=$(wex hook/exec -c=appGo --quiet)
  
  if [ "${COMMAND}" != '' ];then
    COMMAND+=' &&  /bin/bash'
  fi

  # docker attach
  docker exec -it ${CONTAINER} /bin/bash -c "${COMMAND}"
}
