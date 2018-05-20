#!/usr/bin/env bash

siteComposeArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" true'
  )
}

siteCompose() {

  wex config/load

  # Load expected env file.
  local SITE_ENV=$(wex site/env)

  local SERVICES=($(ls ${WEX_DIR_ROOT}"services"))

  # Iterate through array using a counter
  for ((i=0; i<${#SERVICES[@]}; i++)); do
      SERVICE=${SERVICES[$i]}
      SERVICE_UPPERCASE=$(echo ${SERVICE} | tr '[:lower:]' '[:upper:]')
      local VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}"_BASE"
      local YML_INHERIT=${WEX_DIR_ROOT}"services/"${SERVICE}"/docker-compose.yml"
      export ${VAR_NAME}=${YML_INHERIT}

      local VAR_NAME="WEX_COMPOSE_YML_"${SERVICE_UPPERCASE}
      local YML_INHERIT_ENV=${WEX_DIR_ROOT}"services/"${SERVICE}"/docker-compose."${SITE_ENV}".yml"
      if [ -f ${YML_INHERIT_ENV} ];then
        export ${VAR_NAME}=${YML_INHERIT_ENV}
      else
        export ${VAR_NAME}=${YML_INHERIT}
      fi
  done

  if [ $(wex service/used -s=proxy) == false ];then
    local COMPOSE_FILES=" -f "${WEX_DIR_ROOT}"containers/default/docker-compose.yml"
  else
    local COMPOSE_FILES=" -f "${WEX_DIR_ROOT}"containers/network/docker-compose.yml"
  fi

  local FILES=(
    # Base docker file / may extend global container.
    "docker/docker-compose.yml"
  );

  # Local env specific file
  local ENV_YML="docker/docker-compose."${SITE_ENV}".yml"
  if [ -f ${ENV_YML} ];then
    FILES+=(${ENV_YML})
  fi

  for FILE in ${FILES[@]}
  do
    # File exists.
    if [ -f ${FILE} ]; then
      COMPOSE_FILES=${COMPOSE_FILES}" -f "${FILE}
    fi;
  done;

  docker-compose ${COMPOSE_FILES} ${COMMAND}
}
