#!/usr/bin/env bash

siteLoadEnvArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

siteLoadEnv() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Load .env file
  . ${DIR_SITE}".env"
}
