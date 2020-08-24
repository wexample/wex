#!/usr/bin/env bash

configWriteArgs() {
  _ARGUMENTS=(
    'started s "Set the site is started or not" false'
    'no_recreate nr "No recreate if files exists" false'
  )
}

configWrite() {
  # No recreate.
  if [ "${NO_RECREATE}" = true ] &&
    [ -f "${WEX_WEXAMPLE_APP_DIR_TMP}config" ] &&
    [ -f "${WEX_WEXAMPLE_APP_COMPOSE_BUILD_YML}" ];then

    # TODO fix the config issue in globals.sh before enabling nested logs
    #  _wexLog "App config file exists. No recreating."
    return
  fi

  . .wex

  _wexLog "Creating temporary folder : ${WEX_WEXAMPLE_APP_DIR_TMP}"
    # Create temp dirs if not exists.
  mkdir -p "${WEX_WEXAMPLE_APP_DIR_TMP}"

  if [ "${STARTED}" != true ];then
   # Default space separator
    STARTED=false
  fi;

  local APPS_PATHS=$(cat "${WEX_PROXY_APPS_REGISTRY}")
  local PORTS_USED_CURRENT=$(wex service/findFreeLocalPorts -s=",")
  _wexLog "Assign local ports : ${PORTS_USED_CURRENT}"

  local APP_ENV=$(wex app/env)
  local APP_NAME=${NAME}
  local SITE_PATH=$(realpath ./)"/"
  local APP_ENV_MAJ=${APP_ENV^^}
  local DOMAINS=$(eval 'echo ${'${APP_ENV_MAJ}'_DOMAINS}')
  local DOMAIN_MAIN=$(eval 'echo ${'${APP_ENV_MAJ}'_DOMAIN_MAIN}')

  # Support custom images version
  if [ "${IMAGES_VERSION}" == "" ];then
    local IMAGES_VERSION
    IMAGES_VERSION=$(wex core/version)
  fi

  _wexLog "Preparing global site configuration"

  local APP_CONFIG_FILE_CONTENT=""

  # TODO Prefix all with APP_
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

  local USER_UID=${UID}
  # Current user is root, so uid is 0.
  if [ "${USER_UID}" = "0" ];then
    USER_UID=${SUDO_UID}
  fi

  wex config/setValue -k=USER_UID -v=${USER_UID}

  wex config/addTitle -t="Wex"
  wex config/setValue -k=WEX_IMAGES_VERSION -v=${IMAGES_VERSION}

  _wexLog "Calling config hooks"
  wex hook/exec -c="appConfig"

  # In case we are on non unix system.
  wex file/convertLinesToUnix -f="${WEX_WEXAMPLE_APP_FILE_CONFIG}" &> /dev/null

  # Create docker-compose.build.yml
  wex app/compose -c="config" | tee "${WEX_APP_COMPOSE_BUILD_YML}" > /dev/null
}
