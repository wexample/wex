#!/usr/bin/env bash

siteLoadEnvArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root site directory" false'
  )
}

siteLoadEnv() {
  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  # Load .env file
  . ${DIR}".env"
}
