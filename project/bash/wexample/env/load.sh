#!/usr/bin/env bash

envLoadArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

envLoad() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Load .env file
  . ${DIR_SITE}".env"
}
