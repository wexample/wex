#!/usr/bin/env bash

dbRestoreArgs() {
  _ARGUMENTS=(
    [0]='dump d "Dump file to import, in the dumps folder only, asked if missing" false'
    [1]='environment e "Remote environment name" false'
  )
}

dbRestore() {
  # We expect to be into site root folder.

  # This may be improved in the future.
  CONTAINER_PATH_ROOT="/var/www/html"
  CONTAINER_PATH_DUMPS="/var/www/mysql/dumps"

  if [[ $(wex docker/isEnv) == false ]]; then

    # Remote restoration.
    if [ ! -z ${ENVIRONMENT+x} ];then
      # Restore
      wex wexample::remote/exec -e=${ENVIRONMENT} -s="wex db/restore"
      # Complete
      return
    fi;

    if [ -z ${DUMP+x} ];then
      # Ask user to choose a file.
      wex db/dumpChooseList
      # Prompt does not work in the exec terminal.
      DUMP=$(wex db/dumpChoose)
    fi

    # Container should contain wexample script installed.
    wex site/exec -c="wex wexample::db/restore -d=${DUMP}"

  else
    # Go to site root.
    # It enables wexample site context.
    cd ${CONTAINER_PATH_ROOT}

    # Load env name.
    wex env/load

    # Can't load this data into container.
    . ${WEX_WEXAMPLE_SITE_CONFIG}

    # Load credentials stored into config
    wex config/load

    wex framework/settings -d=${CONTAINER_PATH_ROOT}

    # Restore
    wex framework/restore \
      -f=${CONTAINER_PATH_DUMPS}"/"${DUMP} \
      -h=${SITE_NAME}"_mysql" \
      -P=${SITE_DB_PORT} \
      -db=${SITE_DB_NAME} \
      -u=${SITE_DB_USER} \
      -p=${SITE_DB_PASSWORD}
  fi
}
