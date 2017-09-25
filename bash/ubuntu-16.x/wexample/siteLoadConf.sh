#!/usr/bin/env bash

wexampleSiteLoadConfArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root site directory" false'
 )
}

wexampleSiteLoadConf() {
  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  # Load .env file
  . ${DIR}".env"
}
