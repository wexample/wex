#!/usr/bin/env bash

imagesRebuildArgs() {
  _ARGUMENTS=(
    [0]='flush_cache f "Remove existing images before rebuild" false'
    [1]='deploy d "Deploy each built image" false'
    [2]='no_cache c "No cache" false'
    [3]='image_name n "Selected image name only" false'
  )
}

imagesRebuild() {
  cd ${WEX_DIR_ROOT}docker/images/
  WEX_BUILT_IMAGES=()

  # Deploy
  if [[ ${DEPLOY} == true ]]; then
     docker login
  fi;

  if [[ ${FLUSH_CACHE} == true ]]; then
    NO_CACHE=true
    # Remove all images from wexample
    docker rmi $(docker images wexample/* -q)
  fi;

  if [ ! -z "${IMAGE_NAME+x}" ]; then
    _imagesRebuild ${IMAGE_NAME} ${DEPLOY}
  else
    for f in $(ls)
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        _imagesRebuild ${f} ${DEPLOY}
      fi;
    done
  fi;
}

_imagesRebuild() {
  NAME=${1}

  echo "Building ${NAME}"

  DEPENDS_FROM=$(wex config/getValue -f=${NAME}/Dockerfile -k=FROM)
  DEPENDS_FROM_WEX=$(sed -e 's/wexample\/\([^:]*\):.*/\1/' <<< ${DEPENDS_FROM})

  # A manner to avoid non matching strings from sed
  # which are not empty.
  if [ ${DEPENDS_FROM} != ${DEPENDS_FROM_WEX} ];then
    _imagesRebuild ${DEPENDS_FROM_WEX}
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

  CACHE=''
  # If no cache is set.
  if [ ! -z ${NO_CACHE+x} ]; then
    CACHE='--no-cache'
  fi;

  # Build
  docker build -t wexample/${NAME}:latest ${NAME} ${CACHE}

  # Deploy
  if [ ! -z ${DEPLOY+x} ]; then
    docker push wexample/${NAME}:latest
  fi;
}
