#!/usr/bin/env bash

wexampleDockerImagesDeployArgs() {
  _ARGUMENTS=(
    [0]='build b "Rebuild all images before deployment" false'
  )
}

wexampleDockerImagesDeploy() {
  if [ ! -z "${BUILD+x}" ]; then
    wex wexample/dockerImagesRebuild
  fi;

  docker login

  for f in $(ls)
    do
      # Filter only directories.
      if [ -d ${BASE_PATH}${f} ]; then
        docker push wexample/${f}:latest
      fi;
    done
}
