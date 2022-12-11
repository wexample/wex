#!/usr/bin/env bash

appConfigArgs() {
  _ARGUMENTS=(
    'key k "Key of config param to get" true'
    'dir_site d "Root site directory" false'
  )
}

appConfig() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  . .wex

  # Uppercase key.
  eval 'echo ${'${KEY^^}'}'
}
