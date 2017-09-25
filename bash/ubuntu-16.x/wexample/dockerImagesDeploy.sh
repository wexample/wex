#!/usr/bin/env bash

wexampleSiteDumpArgs() {
  _ARGUMENTS=(
    [0]='build b "Rebuild all images before deployment" false'
  )
}

wexampleDockerImagesDeploy() {
  if [ ! -z "${BUILD+x}" ]; then
    wex wexample/dockerImagesRebuild
  fi;

  docker login

  docker push wexample/wexubuntu16:latest
  docker push wexample/wexwebserver:latest
  docker push wexample/wexphp7:latest
}
