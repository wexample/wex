#!/usr/bin/env bash

siteDomainsArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

siteDomains() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  DOCKER_COMPOSE_VARS=$(wex site/configYml)
  ALL_DOMAINS=()

  for DOCKER_COMPOSE_VAR in ${DOCKER_COMPOSE_VARS[@]}
  do
    DOMAINS=$(sed -n "s/^services_web_\(.*\)_\?environment_VIRTUAL_HOST\=\"*\([^\"]*\)\"*\$/\2/p" <<< ${DOCKER_COMPOSE_VAR})

    if [ ! -z "${DOMAINS+x}" ]; then
      # Split multiple domains.
      DOMAINS=($(echo ${DOMAINS} | tr "," "\n"))
      for DOMAIN in ${DOMAINS[@]}
      do
        ALL_DOMAINS+=(${DOMAIN})
      done;
    fi
  done;

  echo ${ALL_DOMAINS[@]}
}
