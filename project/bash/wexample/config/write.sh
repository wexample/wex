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

  SITE_CONFIG_FILE+="\nSITE_PORT_RANGE="$(wex port/rangeGenerate)

  # Execute services scripts if exists
  local CONFIG=$(wex service/exec -c="config")
  SITE_CONFIG_FILE+=${CONFIG[@]}
  # Sync images versions to wex.
  SITE_CONFIG_FILE+="\nWEX_IMAGES_VERSION="$(wex wex/version)

  # Save param file.
  echo -e ${SITE_CONFIG_FILE} > ${WEX_WEXAMPLE_SITE_DIR_TMP}config
  # In case we are on non unix system.
  wex file/convertLinesToUnix -f=./tmp/config &> /dev/null

  echo -e "${SITE_CONFIG_FILE}"

  # Create docker-compose.build.yml
  wex site/compose -c="config" > ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
}
