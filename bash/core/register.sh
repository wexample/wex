#!/usr/bin/env bash

coreRegisterArgs() {
  _DESCRIPTION="Update local unversioned registeries"
  # shellcheck disable=SC2034
  _DESCRIPTION="Create a local core registries."
}

coreRegister() {
  local LOCATIONS=$(_wexFindScriptsLocations)
  local ALL_SCRIPTS=()
  local ALL_SCRIPTS_PATHS=()

  _wexLog "Creating scripts registry..."
  for LOCATION in ${LOCATIONS[@]}; do
    ALL_SCRIPTS+=($(wex-exec scripts/list -d="${LOCATION}"))

    local ADDON=""
    local ADDON_PATH=$(dirname "${LOCATION}")
    if [ $(dirname "${ADDON_PATH}")/ == "${WEX_DIR_ADDONS}" ]; then
      ADDON=$(basename "${ADDON_PATH}")
    elif [ "${ADDON_PATH}/" == "${WEX_DIR_ROOT}" ]; then
      ADDON="default"
    fi

    ALL_SCRIPTS_PATHS+=($(wex-exec scripts/list -d="${LOCATION}" -f -a="${ADDON}"))
  done

  echo "${ALL_SCRIPTS[@]}" | tr ' ' '\n' | sort >"${WEX_FILE_ALL_SCRIPTS}"
  echo "${ALL_SCRIPTS_PATHS[@]}" | tr ' ' '\n' | sort >"${WEX_FILE_ALL_SCRIPTS_PATHS}"

  _wexLog "Creating apps config registry..."

  # Load expected env file.
  local APP_ENV=$(wex-exec app::app/env)
  local SERVICES=($(wex-exec app::services/all))
  local SERVICE_DIR
  local SERVICE_UPPERCASE
  local VAR_NAME
  local YML_INHERIT

  echo "" >"${WEX_DIR_TMP}app-config"
  # Iterate through array using a counter
  for SERVICE in "${SERVICES[@]}"; do
    SERVICE_UPPERCASE=$(wex-exec string/toScreamingSnake -t="${SERVICE}")
    SERVICE_DIR=$(wex-exec service/dir -s="${SERVICE}")

    VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}"_BASE"
    YML_INHERIT="${SERVICE_DIR}docker/docker-compose.yml"
    wex-exec default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${YML_INHERIT}" -vv

    local VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}
    local YML_INHERIT_ENV="${SERVICE_DIR}docker/docker-compose."${APP_ENV}".yml"
    local VAR_VALUE

    if [ -f "${YML_INHERIT_ENV}" ]; then
      VAR_VALUE="${YML_INHERIT_ENV}"
    else
      VAR_VALUE="${YML_INHERIT}"
    fi

    wex-exec default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${VAR_VALUE}" -vv
  done
}
