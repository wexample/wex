#!/usr/bin/env bash

configWriteArgs() {
  _AS_NON_SUDO=false
  _ARGUMENTS=(
    'started s "Set the site is started or not" false'
    'no_recreate nr "No recreate if files exists" false'
  )
}

configWrite() {
  # No recreate.
  if [ "${NO_RECREATE}" == true ] &&
    [ -f ${WEX_WEXAMPLE_APP_DIR_TMP}config ] &&
    [ -f ${WEX_WEXAMPLE_APP_COMPOSE_BUILD_YML} ];then

    _wexLog "App config file exists. No recreating."
    return
  fi

  . .wex

  _wexLog "Creating temporary folder : ${WEX_WEXAMPLE_APP_DIR_TMP}"
    # Create temp dirs if not exists.
  mkdir -p ${WEX_WEXAMPLE_APP_DIR_TMP}

  if [ "${STARTED}" != true ];then
   # Default space separator
    STARTED=false
  fi;

  local APPS_PATHS=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  local PORTS_USED_CURRENT=$(wex service/findFreeLocalPorts -s=",")
  _wexLog "Assign local ports : ${PORTS_USED_CURRENT}"

  local APP_ENV=$(wex site/env)
  local APP_NAME=${NAME}
  local SITE_PATH=$(realpath ./)"/"
  local APP_ENV_MAJ=${APP_ENV^^}
  local DOMAINS=$(eval 'echo ${'${APP_ENV_MAJ}'_DOMAINS}')
  local DOMAIN_MAIN=$(eval 'echo ${'${APP_ENV_MAJ}'_DOMAIN_MAIN}')

  # Support custom images version
  if [ "${IMAGES_VERSION}" == "" ];then
    local IMAGES_VERSION=$(wex wex/version)
  fi

  _wexLog "Preparing global site configuration"

  local APP_CONFIG_FILE_CONTENT=""

  # TODO Previx all with APP_
  APP_CONFIG_FILE_CONTENT+='\n# App'
  APP_CONFIG_FILE_CONTENT+='\nAPP_NAME_INTERNAL='${APP_NAME}"_"${APP_ENV}
  APP_CONFIG_FILE_CONTENT+='\nSITE_PORTS_USED='${PORTS_USED_CURRENT}
  APP_CONFIG_FILE_CONTENT+='\nSITE_NAME='${APP_NAME}
  APP_CONFIG_FILE_CONTENT+='\nSITE_NAME_INTERNAL='${APP_NAME}"_"${APP_ENV}
  APP_CONFIG_FILE_CONTENT+='\nSITE_ENV='${APP_ENV}
  APP_CONFIG_FILE_CONTENT+='\nSTARTED='${STARTED}
  APP_CONFIG_FILE_CONTENT+='\nDOMAIN_MAIN='${DOMAIN_MAIN}
  APP_CONFIG_FILE_CONTENT+='\nDOMAINS='${DOMAINS}
  APP_CONFIG_FILE_CONTENT+='\nEMAIL='$(eval 'echo ${'${APP_ENV_MAJ}'_EMAIL}')

  _wexLog "Wrinting config file content"
  echo -e ${APP_CONFIG_FILE_CONTENT} | tee ${WEX_WEXAMPLE_APP_FILE_CONFIG} > /dev/null

  wex config/addTitle -t="User"
  wex config/setValue -k=USER_UID -v=${UID}

  wex config/addTitle -t="Wex"
  wex config/setValue -k=WEX_IMAGES_VERSION -v=${IMAGES_VERSION}

  _wexLog "Calling config hooks"
  wex hook/exec -c="appConfig"

  # In case we are on non unix system.
  wex file/convertLinesToUnix -f=${WEX_WEXAMPLE_APP_FILE_CONFIG} &> /dev/null

  # Create docker-compose.build.yml
  wex site/compose -c="config" | tee ${WEX_APP_COMPOSE_BUILD_YML} > /dev/null
}
