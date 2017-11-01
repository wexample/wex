#!/usr/bin/env bash

wexampleSiteDockerAttachArgs() {
  _ARGUMENTS=(
    [0]='container c "Docker container suffix" true'
    [1]='dir d "Root directory of site" false'
  )
}

wexampleSiteDockerAttach() {

  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);

  # Containers without tty can't be attached, so we run bash
  docker exec -t -i ${SITE_NAME}_${CONTAINER} /bin/bash
}
