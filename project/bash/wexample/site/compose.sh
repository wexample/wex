#!/usr/bin/env bash

siteComposeArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" true'
  )
}

siteCompose() {

  wex config/load

  # Load expected env file.
  . .env

  local SERVICES=($(ls ${WEX_DIR_ROOT}"docker/services"))

  # Iterate through array using a counter
  for ((i=0; i<${#SERVICES[@]}; i++)); do
      SERVICE=${SERVICES[$i]}
      SERVICE_UPPERCASE=$(echo ${SERVICE} | tr '[:lower:]' '[:upper:]')
      VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}"_BASE"
      export ${VAR_NAME}=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/docker-compose.yml"

      VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}
      export ${VAR_NAME}=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/docker-compose."${SITE_ENV}".yml"
  done

  COMPOSE_FILES=" -f "${WEX_DIR_ROOT}"docker/containers/default/docker-compose.yml"

  FILES=(
    # Base docker file / may extend global container.
    "docker/docker-compose.yml"
    # Local env specific file
    "docker/docker-compose."${SITE_ENV}".yml"
  );

  for FILE in ${FILES[@]}
  do
    # File exists.
    if [ -f ${FILE} ]; then
      COMPOSE_FILES=${COMPOSE_FILES}" -f "${FILE}
    fi;
  done;

  docker-compose ${COMPOSE_FILES} ${COMMAND}
}
