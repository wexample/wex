#!/usr/bin/env bash

coreRegisterArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Create a local core registries."
}

coreRegister() {
  _coreRegisterScripts
  _coreRegisterConfig
  _coreRegisterConfigMiddlewares
}

_coreRegisterScripts() {
  local ALL_SCRIPTS=()
  local ALL_SCRIPTS_PATHS=()
  local LOCATIONS

  _wexLog "Creating scripts registry..."

  LOCATIONS=$(_wexFindScriptsLocations)

  for LOCATION in ${LOCATIONS[@]}; do
    ALL_SCRIPTS+=($(wex-exec scripts/list -d="${LOCATION}"))

    local ADDON=$(_wexGetAddonFromPath "${LOCATION}")

    ALL_SCRIPTS_PATHS+=($(wex-exec scripts/list -d="${LOCATION}" -f -a="${ADDON}"))
  done

  echo "${ALL_SCRIPTS[@]}" | tr ' ' '\n' | sort >"${WEX_FILE_ALL_SCRIPTS}"
  echo "${ALL_SCRIPTS_PATHS[@]}" | tr ' ' '\n' | sort >"${WEX_FILE_ALL_SCRIPTS_PATHS}"
}

_coreRegisterConfig() {
  # Load expected env file.
  local APP_ENV=$(wex-exec app::app/env)
  local SERVICES=($(wex-exec app::services/all))
  local SERVICE_DIR
  local SERVICE_UPPERCASE
  local VAR_NAME
  local YML_INHERIT

  _wexLog "Creating apps config registry..."

  echo "" >"${WEX_DIR_TMP}app-config"
  # Iterate through array using a counter
  for SERVICE in "${SERVICES[@]}"; do
    SERVICE_UPPERCASE=$(wex-exec string/toScreamingSnake -t="${SERVICE}")
    SERVICE_DIR=$(wex-exec service/dir -s="${SERVICE}")

    VAR_NAME="WEX_COMPOSE_YML_${SERVICE_UPPERCASE}_BASE"
    YML_INHERIT="${SERVICE_DIR}docker/docker-compose.yml"
    wex-exec default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${YML_INHERIT}" -vv

    local VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}
    local YML_INHERIT_ENV="${SERVICE_DIR}docker/docker-compose.${APP_ENV}.yml"
    local VAR_VALUE

    if [ -f "${YML_INHERIT_ENV}" ]; then
      VAR_VALUE="${YML_INHERIT_ENV}"
    else
      VAR_VALUE="${YML_INHERIT}"
    fi

    wex-exec default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${VAR_VALUE}" -vv
  done
}

_coreRegisterConfigMiddlewares() {
  local ADDONS_DIRS
  local MIDDLEWARE
  local OUTPUT=()
  ADDONS_DIRS=$(_wexFindAddonsDirs)

  for DIR in ${ADDONS_DIRS[@]}; do
    MIDDLEWARE="${DIR}bash/middleware.sh"
    if [ -f "${MIDDLEWARE}" ]; then
      OUTPUT+=("${MIDDLEWARE}")
    fi
  done

  printf "%s\n" "${OUTPUT[@]}" >"${WEX_FILE_MIDDLEWARES}"
}
