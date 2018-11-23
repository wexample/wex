#!/usr/bin/env bash

siteDomainsArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
    [1]='separator s "Separator" false'
  )
}

siteDomains() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  DOCKER_COMPOSE_VARS=($(wex config/yml -d=${DIR_SITE}))
  ALL_DOMAINS=''

  if [ -z "${SEPARATOR+x}" ];then
    SEPARATOR=" "
  fi;

  for DOCKER_COMPOSE_VAR in ${DOCKER_COMPOSE_VARS[@]}
  do
    DOMAINS=$(sed -n "s/^services_\(.\{0,\}\)_\?environment_VIRTUAL_HOST\=\"\{0,\}\([^\"]\{0,\}\)\"\{0,\}\$/\2/p" <<< ${DOCKER_COMPOSE_VAR})

    if [ ! -z "${DOMAINS+x}" ]; then
      # Split multiple domains.
      DOMAINS=($(echo ${DOMAINS} | tr "," "\n"))
      for DOMAIN in ${DOMAINS[@]}
      do
        # Add separator.
        if [ "${ALL_DOMAINS}" != "" ];then
          ALL_DOMAINS+=${SEPARATOR}
        fi;
        ALL_DOMAINS+=${DOMAIN}
      done;
    fi
  done;

  echo ${ALL_DOMAINS}
}
