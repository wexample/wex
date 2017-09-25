#!/usr/bin/env bash

wexampleDockerImagesRebuildArgs() {
  _ARGUMENTS=(
    [0]='flush_cache f "Use --no-cache option" false'
  )
}

wexampleDockerImagesRebuild() {
  cd ${WEX_DIR_ROOT}docker/
  WEX_DOCKER_BUILT=

  if [ -z ${FLUSH_CACHE+x} ]; then
    # Remove all images from wexample
    docker rmi $(docker images wexample/* -q)
  fi;

  for f in $(ls)
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        _wexampleDockerImagesRebuild ${f} ${FLUSH_CACHE}
      fi;
    done
}

_wexampleDockerImagesRebuild() {
  NAME=${1}

  echo "Building ${NAME}"

  DEPENDS_FROM=$(wex config/getValue -f=${NAME}/Dockerfile -k=FROM)
  DEPENDS_FROM_WEX=$(sed -e 's/wexample\/\([^:]*\):.*/\1/' <<< ${DEPENDS_FROM})

  # A manner to avoid non matching strings from sed
  # which are not empty.
  if [ ${DEPENDS_FROM} != ${DEPENDS_FROM_WEX} ];then
    _wexampleDockerImagesRebuild ${DEPENDS_FROM_WEX}
  fi;

  # Need to redeclare after recursion.
  NAME=${1}

  # We resolve dependencies but we have not succeed
  # to avoid rebuilding the same parent image multiple times.
  docker build -t wexample/${NAME}:latest ${NAME} ${USE_CACHE}
}
