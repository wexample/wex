#!/usr/bin/env bash

dockerComposeArgs() {
 _ARGUMENTS=(
   [0]='env e "Environment name for ext of docker-compose.ext.yml" false'
 )
}

dockerCompose() {
  COMMAND="docker-compose -f docker-compose.yml"

  # There is an env arg.
  if [ ! -z "${ENV+x}" ];then
    # Default space separator
    COMMAND=${COMMAND}" -f docker-compose."${ENV}".yml"
  fi;

  COMMAND=${COMMAND}" up -d --build"

  ${COMMAND}
}
