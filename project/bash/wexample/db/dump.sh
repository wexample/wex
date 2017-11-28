#!/usr/bin/env bash

dbDumpArgs() {
  _ARGUMENTS=(
    [0]='site_name n "Website name (internal usage for container execution)" false'
    [1]='site_env e "Website environment (internal usage for container execution)" false'
    [2]='latest l "Save latest copy file" false'
  )
}

dbDump() {
  # We expect to be into site root folder.

  # This may be improved in the future.
  CONTAINER_PATH_ROOT="/var/www/html"
  CONTAINER_PATH_DUMPS="/var/dumps"

  # We are not into the docker container.
  # So we will access to it in order to re-execute current command.
  if [[ $(wex docker/isEnv) == false ]]; then

    # Container should contain wexample script installed.
    wex site/exec -c="wex wexample::db/dump -l=${LATEST}"

  else
    # Go to site root.
    # It enables wexample site context.
    cd ${CONTAINER_PATH_ROOT}

    # Load env name.
    wex site/loadEnv

    # Can't load this data into container.
    . ${WEX_WEXAMPLE_SITE_CONFIG}

    wex framework/settings -d=${CONTAINER_PATH_ROOT}

    # Don't use zip_only so we keep original sql file as return.
    DUMP_FILE=$(wex framework/dump \
      -s=${CONTAINER_PATH_ROOT} \
      -d=${CONTAINER_PATH_DUMPS} \
      --prefix=${SITE_ENV}"-" \
      -H=${SITE_NAME}"_mysql" \
      -P=${SITE_DB_PORT} \
      -db=${SITE_DB_NAME} \
      -u=${SITE_DB_USER} \
      -p=${SITE_DB_PASSWORD} \
      -zip);

    if [ -z ${DUMP+x} ];then
      LATEST_DUMP_FILE=${CONTAINER_PATH_DUMPS}"/"${SITE_ENV}"-"${SITE_NAME}"-latest.sql"
      # Clone to latest
      cp ${DUMP_FILE} ${LATEST_DUMP_FILE}
      # Create zip.
      zip ${LATEST_DUMP_FILE}".zip" ${LATEST_DUMP_FILE} -q -j
      # No more usage of source files.
      rm -f ${LATEST_DUMP_FILE}
    fi;

    # No more usage of source files.
    rm -f ${DUMP_FILE}

    echo ${DUMP_FILE}
  fi;
}
