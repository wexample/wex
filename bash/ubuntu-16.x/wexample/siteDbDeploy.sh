#!/usr/bin/env bash

wexampleSiteDbDeployArgs() {
  _ARGUMENTS=(
    [0]='env e "Destination environment" false' # TODO
    [1]='dir d "Root directory of site" false'
  )
}

wexampleSiteDbDeploy() {
  ${ENV}

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
    docker exec ${WEB_CONTAINER} wex wexample/siteDbDeploy "$@" -d=${CONTAINER_PATH_ROOT}

    # Stop website.
    if [[ ${STARTED} == true ]];then
      docker-compose down
    fi;

  else
    echo "Go to prod";

    DUMPS_DIR="/var/www/dumps"

    # TODO For now we use latest path but we may choose which one
    LATEST_DUMP_FILE=${DUMPS_DIR}"/"$(wex wexample/siteDbDumpLatestFileName -d=${DIR})".zip"

    SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);
    DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployIpv4);
    DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployPort);
    DEPLOY_USER=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployUser);
    PROD_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=prodPathRoot);

    wex wexample/siteScpUpload -d=${DIR} -f=${LATEST_DUMP_FILE}
    # TODO
    wex wexample/siteSshExec -d=${DIR} -c="sudo wex hi"
  fi;
}
