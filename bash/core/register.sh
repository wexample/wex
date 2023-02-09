#!/usr/bin/env bash

coreRegisterArgs() {
  _DESCRIPTION="Create a local core registries."
}

coreRegister() {
  local LOCATIONS=$(_wexFindScriptsLocations)
  local ALL_SCRIPTS=()

  _wexLog "Creating scripts registry..."
  for LOCATION in ${LOCATIONS[@]}; do
    ALL_SCRIPTS+=($(wex scripts/list -d="${LOCATION}"))
  done

  echo "${ALL_SCRIPTS[@]}" | tr ' ' '\n' | sort > "${WEX_DIR_TMP}all-scripts"

  _wexLog "Creating apps config registry..."

  # Load expected env file.
  local APP_ENV=$(wex app::app/env)
  local SERVICES=($(wex app::services/all))
  local SERVICE_DIR
  local SERVICE_UPPERCASE
  local VAR_NAME
  local YML_INHERIT

  echo "" > "${WEX_DIR_TMP}app-config"
  # Iterate through array using a counter
  for SERVICE in "${SERVICES[@]}"
  do
      SERVICE_UPPERCASE=$(wex string/toScreamingSnake -t="${SERVICE}")
      SERVICE_DIR=$(wex service/dir -s="${SERVICE}")

      VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}"_BASE"
      YML_INHERIT="${SERVICE_DIR}docker/docker-compose.yml"
      wex default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${YML_INHERIT}" -vv

      local VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}
      local YML_INHERIT_ENV="${SERVICE_DIR}docker/docker-compose."${APP_ENV}".yml"
      local VAR_VALUE

      if [ -f "${YML_INHERIT_ENV}" ];then
        VAR_VALUE="${YML_INHERIT_ENV}"
      else
        VAR_VALUE="${YML_INHERIT}"
      fi

      wex default::config/setValue -i -s="=" -f="${WEX_DIR_TMP}app-config" -k="${VAR_NAME}" -v="${VAR_VALUE}" -vv
  done
}
