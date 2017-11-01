#!/usr/bin/env bash

wexampleSiteDbRestoreArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
  )
}

wexampleSiteDbRestore() {
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
    docker exec ${WEB_CONTAINER} wex wexample/siteDbRestore "$@" -d=${CONTAINER_PATH_ROOT}

    # Stop website.
    if [[ ${STARTED} == true ]];then
      docker-compose down
    fi;

  else

    # Choose between argument or latest dump.
    if [ ! -z "${1+x}" ]; then
      DUMP_FILE=${1}
    else
      DUMP_FILE=$(wex wexample/siteDbDumpLatestFileName)".gz"
    fi;

    DUMPS_DIR="/var/www/dumps"

    LATEST_DUMP_FILE=${DUMPS_DIR}"/"$(wex wexample/siteDbDumpLatestFileName -d=${DIR})".zip"

    # Restore
    wex framework/restore \
      -f=${LATEST_DUMP_FILE} \
      -H=${SITE_NAME}"_mysql" \
      -P=${HOST_MYSQL_PORT} \
      -db=${SITE_NAME} \
      -u=${HOST_MYSQL_USER} \
      -p=${HOST_MYSQL_PASSWORD}
  fi;
}
