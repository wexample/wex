#!/usr/bin/env bash

siteComposeArgs() {
 _ARGUMENTS=(
   [0]='command c "Command to execute" true'
 )
}

siteCompose() {
  # Load expected env file.
  . .env

  FILES=(
    # Base docker file / may extend global container.
    "docker/docker-compose.yml"
    # Global env specific file
    ${WEX_DIR_ROOT}"samples/docker/docker-compose."${SITE_ENV}".yml"
    # Local env specific file
    "docker/docker-compose."${SITE_ENV}".yml"
  );

  COMPOSE="docker-compose"

  for FILE in ${FILES[@]}
  do
    # File exists.
    if [ -f ${FILE} ]; then
        COMPOSE=${COMPOSE}" -f "${FILE}
    fi;
  done;

  # Global variables
  export SITE_NAME=$(wex site/config -k=name)
  export WEX_COMPOSE_YML=${WEX_DIR_ROOT}"samples/docker/docker-compose.yml"
  export WEX_SCRIPTS_PATH=${WEX_DIR_ROOT}

  # Get framework specific settings.
  wex framework/settings -d="project"

  # Expose settings.
  export SITE_DB_HOST=${SITE_DB_HOST}
  export SITE_DB_NAME=${SITE_DB_NAME}
  export SITE_DB_USER=${SITE_DB_USER}
  export SITE_DB_PASSWORD=${SITE_DB_PASSWORD}

  ${COMPOSE} ${COMMAND}
}
