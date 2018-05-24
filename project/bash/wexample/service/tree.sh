#!/usr/bin/env bash

serviceTreeArgs() {
  _ARGUMENTS=(
    [0]='services s "Services list, comma separated" true'
  )
}

serviceTree() {
  #  local SERVICES_JOINED=${SERVICES}
  local SERVICES_LIST=($(echo ${SERVICES} | tr "," "\n"))
  local SERVICES_JOINED=''

  for SERVICE in ${SERVICES_LIST[@]}
  do
    if [ "${SERVICES_JOINED}" != "" ];then
      SERVICES_JOINED+=','
    fi

    SERVICES_JOINED+=${SERVICE}

    local SERVICE_CONFIG=${WEX_DIR_ROOT}"services/"${SERVICE}"/config"
    local DEPENDENCIES=false
    if [ -f ${SERVICE_CONFIG} ];then
      # Load conf file.
      . ${SERVICE_CONFIG}
      if [ ${DEPENDENCIES} != false ];then
        SERVICES_JOINED+=','$(wex service/tree -s=${DEPENDENCIES})
      fi
    fi
  done

  # Remove duplicates
  local SERVICES_LIST=($(echo ${SERVICES_JOINED} | tr "," "\n"))
  local SERVICES_ADDED_LIST=()
  local SERVICES_JOINED=''

  # Loop all services.
  for SERVICE in ${SERVICES_LIST[@]}
  do
    local FOUND=false

    # Loop already added.
    for SERVICE_ADDED in ${SERVICES_ADDED_LIST[@]}
    do
      if [ "${SERVICE_ADDED}" == "${SERVICE}" ];then
        FOUND=true
      fi
    done

    if [ ${FOUND} == false ];then
      SERVICES_ADDED_LIST+=(${SERVICE})
      if [ "${SERVICES_JOINED}" != "" ];then
        SERVICES_JOINED+=','
      fi
      SERVICES_JOINED+=${SERVICE}
    fi
  done

  echo ${SERVICES_JOINED}
}
