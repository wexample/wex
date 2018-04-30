#!/usr/bin/env bash

imagesRebuildArgs() {
  _ARGUMENTS=(
    [0]='flush_cache f "Remove existing images before rebuild" false'
    [1]='deploy d "Deploy each built image" false'
    [2]='no_cache c "No cache" false'
    [3]='image_name n "Selected image name only" false'
    [4]='docker_username u "Username on docker hub" false'
    [5]='docker_password p "Password on docker hub" false'
    [6]='lsc lsc "Use local stored credentials" false'
    [7]='quiet q "Quiet" false'
  )
}

imagesRebuild() {
  WEX_BUILT_IMAGES=()
  # Set build context
  cd ${WEX_DIR_ROOT}../

  # Deploy
  if [[ ${DEPLOY} == true ]]; then
    # Check integrity to keep versions up to date.

    # We should not have uncommited changes.
    if [ $(wex git/hasChanges) == true ];then
      echo "Wex directory has uncommited changes."
      return
    fi
    # We should not hav unpushed changes.
    if [ $(wex git/hasChanges) == true ];then
      echo "Wex directory has no pushed changes."
      return
    fi

    if [ ! -z "${LSC+x}" ]; then
      DOCKER_USERNAME=$(wex default::var/localGet -n=DOCKER_USERNAME -ask="Docker username for wex images deployment")
      DOCKER_PASSWORD=$(wex default::var/localGet -n=DOCKER_PASSWORD -ask="Docker password" -p)
    else
      if [ ! -z "${DOCKER_USERNAME+x}" ]; then
        DOCKER_USERNAME='-u '${DOCKER_USERNAME}
      fi

      if [ ! -z "${DOCKER_PASSWORD+x}" ]; then
        DOCKER_PASSWORD='-p '${DOCKER_PASSWORD}
      fi
    fi

    docker login ${DOCKER_USERNAME} ${DOCKER_PASSWORD}
  fi;

  if [[ ${FLUSH_CACHE} == true ]]; then
    NO_CACHE=true
    # Remove all images from wexample
    docker rmi $(docker images wexample/* -q)
  fi;

  if [ ! -z "${IMAGE_NAME+x}" ]; then
    _imagesRebuild ${IMAGE_NAME} ${DEPLOY}
  else
    local IMAGES=($(ls project/docker/images/))

    for f in ${IMAGES[@]}
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        _imagesRebuild ${f} ${DEPLOY}
      fi;
    done
  fi;
}

_imagesRebuild() {
  local NAME=${1}
  local DIR=project/docker/images/${NAME}/
  local DOCKERFILE=${DIR}Dockerfile

  echo "Building ${NAME}"

  DEPENDS_FROM=$(wex config/getValue -f=${DOCKERFILE} -k=FROM)
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

  # Use wex version as tag
  local TAG_BASE=wexample/${NAME}
  local TAG=$(wex wex/version)

  if [ "${QUIET}" == true ]; then
    QUIET='-q'
  fi;

  # Build
  docker build ${QUIET} -t ${TAG_BASE}:${TAG} -t ${TAG_BASE}:latest -f ${DOCKERFILE} . ${CACHE}

  # Deploy
  if [ ! -z ${DEPLOY+x} ]; then
    docker push wexample/${NAME}:${TAG}
    docker push wexample/${NAME}:latest
  fi;
}
