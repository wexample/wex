#!/usr/bin/env bash

wexampleDockerImagesRebuildArgs() {
  _ARGUMENTS=(
    [0]='flush_cache f "Remove existing images before rebuild" false'
    [1]='deploy d "Deploy each built image" false'
  )
}

wexampleDockerImagesRebuild() {
  cd ${WEX_DIR_ROOT}docker/
  WEX_BUILT_IMAGES=()

  # Deploy
  if [ ! -z ${DEPLOY+x} ]; then
     docker login
  fi;

  if [ ! -z ${FLUSH_CACHE+x} ]; then
    # Remove all images from wexample
    docker rmi $(docker images wexample/* -q)
  fi;

  for f in $(ls)
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        _wexampleDockerImagesRebuild ${f} ${DEPLOY}
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

  # Check if image has already been built.
  for i in ${WEX_BUILT_IMAGES[@]}; do
    if [[ "$i" = "${NAME}" ]]; then
      echo "  OK : "${i}
      return
      break
    fi
  done

  WEX_BUILT_IMAGES=${WEX_BUILT_IMAGES}" "${1}

  # Build
  docker build -t wexample/${NAME}:latest ${NAME} --no-cache

  # Deploy
  if [ ! -z ${DEPLOY+x} ]; then
    docker push wexample/${NAME}:latest
  fi;
}
