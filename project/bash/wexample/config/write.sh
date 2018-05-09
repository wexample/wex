#!/usr/bin/env bash

configWriteArgs() {
  _ARGUMENTS=(
    [0]='started s "Set the site is started or not" false'
    [1]='no_recreate nr "No recreate if files exists" false'
  )
}

configWrite() {

  # No recreate.
  if [ "${NO_RECREATE}" == true ] &&
    [[ -f ${WEX_WEXAMPLE_SITE_DIR_TMP}config ]] &&
    [[ -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} ]];then
    return
  fi

  # Create temp dirs if not exists.
  mkdir -p ${WEX_WEXAMPLE_DIR_TMP}
  mkdir -p ${WEX_WEXAMPLE_SITE_DIR_TMP}

  if [ "${STARTED}" != true ];then
    # Default space separator
    STARTED=false
  fi;

  # Get site env name.
  . .env
  # Load site base info.
  . .wex

  local SITE_CONFIG_FILE=""
  local SITE_PATH=$(realpath ./)"/"
  SITE_CONFIG_FILE+="\nSITE_NAME="${NAME}
  SITE_CONFIG_FILE+="\nSITE_ENV="${SITE_ENV}
  SITE_CONFIG_FILE+="\nSTARTED="${STARTED}

  # Build ports variables
  local SITES_PATHS=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  local PORTS_USED=$(wex ports/opened -s=",")
  # Avoid common used ports
  PORTS_USED+=",8080,8888"

  # Load used ports in all sites.
  for SITE_PATH in ${SITES_PATHS[@]}
  do
    # Config file exists
    if [ -f ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG} ];then
      # Load config
      . ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}
      if [ "${STARTED}" == true ] && [ ! -z "${SITE_PORTS_USED+x}" ];then
        PORTS_USED+=","${SITE_PORTS_USED}
      fi
    fi
  done

  local SERVICES=($(wex service/list))
  # Some services does not work with ports under 1000
  local PORT_CURRENT=1000
  # Split manually ports list to avoid lines breaks issues.
  local PORTS_USED_ARRAY=$(echo ${PORTS_USED} | sed "s/,/ /g")
  local PORTS_USED_CURRENT=''

  # Assign free ports.
  for SERVICE in ${SERVICES[@]}
  do
    local VAR_NAME=SERVICE_PORT_$(wex text/uppercase -t=${SERVICE})

    # Avoid used ports.
    while [ $(wex array/contains -a="${PORTS_USED_ARRAY[@]}" -i="${PORT_CURRENT}") == true ];do
      ((PORT_CURRENT++))
    done

    # Assign port to variable
    SITE_CONFIG_FILE+="\n"${VAR_NAME}"="${PORT_CURRENT}

    if [ "${PORTS_USED_CURRENT}" != '' ];then
      PORTS_USED_CURRENT+=','
    fi

    PORTS_USED_CURRENT+=${PORT_CURRENT}

    ((PORT_CURRENT++))
  done
  # Save list of used ports.
  SITE_CONFIG_FILE+="\nSITE_PORTS_USED="${PORTS_USED_CURRENT}

  # Execute services scripts if exists
  local CONFIG=$(wex service/exec -c="config")
  SITE_CONFIG_FILE+=${CONFIG[@]}
  # Sync images versions to wex.
  SITE_CONFIG_FILE+="\nWEX_IMAGES_VERSION="$(wex wex/version)

  # Save param file.
  echo -e ${SITE_CONFIG_FILE} > ${WEX_WEXAMPLE_SITE_DIR_TMP}config
  # In case we are on non unix system.
  wex file/convertLinesToUnix -f=./tmp/config &> /dev/null

  # Create docker-compose.build.yml
  wex site/compose -c="config" > ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
}
