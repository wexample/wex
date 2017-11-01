#!/usr/bin/env bash

wexampleSiteDbDumpArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
  )
}

wexampleSiteDbDump() {
  # Wexample uses .env files on websites root to define variables
  # used globally by Docker and also available to define information about
  # data storage or containers connexion.

  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  # Conf contains site name / env and dump directory
  wex wexample/siteLoadConf -d=${DIR}

  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);

  # We are not into the docker container.
  # So we will access to it in order to re-execute current command.
  if [[ $(wex docker/isEnv) == false ]]; then
    WEB_CONTAINER=${SITE_NAME}"_web"
    # Save if we had to start website manually
    # it will stop it at end.
    STARTED=false

    # Start website.
    if [[ $(wex docker/containerRuns -c=${WEB_CONTAINER}) == false ]];then
      STARTED=true
      wex docker/compose -e=${SITE_ENV}
    fi;

    CONTAINER_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=containerPathRoot);

    # Container should contain wexample script installed.
    docker exec ${WEB_CONTAINER} wex wexample/siteDbDump "$@" -d=${CONTAINER_PATH_ROOT}

    # Stop website.
    if [[ ${STARTED} == true ]];then
      docker-compose down
    fi;

  else

    # Check required var exists
    if [[ -z "${DATA_DUMPS_PATH+x}" || -z "${SITE_ENV+x}" ]];then
      exit 1;
    fi;

    DUMPS_DIR="/var/www/dumps"

    # Don't use zip_only so we keep original sql file as return.
    DUMP_FILE=$(wex framework/dump \
      -s=${DIR} \
      -d=${DUMPS_DIR} \
      --prefix=${SITE_ENV}"-" \
      -H=${SITE_NAME}"_mysql" \
      -P=${HOST_MYSQL_PORT} \
      -db=${SITE_NAME} \
      -u=${HOST_MYSQL_USER} \
      -p=${HOST_MYSQL_PASSWORD} \
      -zip);

    LATEST_DUMP_FILE=${DUMPS_DIR}"/"$(wex wexample/siteDbDumpLatestFileName -d=${DIR})

    # Clone to latest
    cp ${DUMP_FILE} ${LATEST_DUMP_FILE}

    # Create zip.
    zip ${LATEST_DUMP_FILE}".zip" ${LATEST_DUMP_FILE} -q -j

    # No more usage of source files.
    rm -rf ${DUMP_FILE}
    rm -rf ${LATEST_DUMP_FILE}

    echo ${DUMP_FILE}
  fi;
}

