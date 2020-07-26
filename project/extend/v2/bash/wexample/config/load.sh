#!/usr/bin/env bash

configLoadArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

configLoad() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  ${WEX_DIR_V3_CMD} config/write -nr

  # Export all variable from conf file.
  set -a
    source ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG}
  set +a

  export SITE_PATH_ROOT=$(realpath ${DIR_SITE})"/"

  # Expose settings.
  export MYSQL_DB_HOST=${MYSQL_DB_HOST}
  export MYSQL_DB_NAME=${MYSQL_DB_NAME}
  export MYSQL_DB_USER=${MYSQL_DB_USER}
  export MYSQL_DB_PASSWORD=${MYSQL_DB_PASSWORD}
  export SERVER_IP=$(wex system/ip)
  export DOMAIN_MAIN=${DOMAIN_MAIN}
  export DOMAINS=${DOMAINS}
  export EMAIL=${EMAIL}
}
