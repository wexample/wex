#!/usr/bin/env bash
wexampleDockerImagesDeployArgs() {
  _ARGUMENTS=(
    [0]='build b "Rebuild all images before deployment" false'
    [1]='flush_cache f "Remove existing images before rebuild" false'
  )
}

wexampleDockerImagesDeploy() {
  docker login

  if [ ! -z "${BUILD+x}" ]; then
    wex wexample/dockerImagesRebuild ${FLUSH_CACHE}
  fi;

  for f in $(ls)
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        docker push wexample/${f}:latest
      fi;
    done
}
