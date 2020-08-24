#!/usr/bin/env bash

serviceFindFreeLocalPortsArgs() {
  _ARGUMENTS=(
    'separator s "Separator" false " "'
  )
}

serviceFindFreeLocalPorts() {
  # Build ports variables
  local PORTS_USED=$(wex ports/opened -s=",")
  # Avoid common used ports
  PORTS_USED+=",8080,8888,21"

  # Load used ports in all sites.
  for SITE_PATH in ${APPS_PATHS[@]}
  do
    # Config file exists
    if [ -f ${SITE_PATH}${WEX_APP_CONFIG} ];then
      # Load config
      . ${SITE_PATH}${WEX_APP_CONFIG}
      if [ "${STARTED}" == true ] && [ ! -z "${SITE_PORTS_USED+x}" ];then
        PORTS_USED+=","${SITE_PORTS_USED}
      fi
    fi
  done

  local SERVICES=($(wex service/list))

  local PREFERRED_PORT=$(eval 'echo ${'${APP_ENV_MAJ}'_PREFERRED_PORT}')
  if [ "${PREFERRED_PORT}" != "" ];then
    # Some services does not work with ports under 1000
    local PORT_CURRENT=${PREFERRED_PORT}
  else
    local PORT_CURRENT=1001
  fi
  # Split manually ports list to avoid lines breaks issues.
  local PORTS_USED_ARRAY=$(echo ${PORTS_USED} | sed "s/,/ /g")
  local PORTS_USED_CURRENT=''

  # Assign free ports.
  for SERVICE in ${SERVICES[@]}
  do
    local VAR_NAME=SERVICE_PORT_${SERVICE^^}

    # Avoid used ports.
    while [[ " ${PORTS_USED_ARRAY[@]} " =~ " ${PORT_CURRENT} " ]];do
      ((PORT_CURRENT++))
    done

    # Assign port to variable
    APP_CONFIG_FILE_CONTENT+="\n"${VAR_NAME}"="${PORT_CURRENT}

    if [ "${PORTS_USED_CURRENT}" != '' ];then
      PORTS_USED_CURRENT+=${SEPARATOR}
    fi

    PORTS_USED_CURRENT+=${PORT_CURRENT}

    ((PORT_CURRENT++))
  done

  echo ${PORTS_USED_CURRENT}
}