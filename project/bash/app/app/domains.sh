#!/usr/bin/env bash

appDomainsArgs() {
  _ARGUMENTS=(
    'dir_site d "Root site directory" false'
    'separator s "Separator" false'
  )
}

appDomains() {
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
    DOMAINS=$(sed -n "s/^services_\(.\{0,\}\)_environment_VIRTUAL_HOST\=\"\{0,\}\([^\"]\{0,\}\)\"\{0,\}\$/\2/p" <<< ${DOCKER_COMPOSE_VAR})

    if [ ! -z "${DOMAINS+x}" ]; then
      # Split multiple domains.
      DOMAINS=($(echo "${DOMAINS}" | tr "," "\n"))
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

  echo "${ALL_DOMAINS}"
}
