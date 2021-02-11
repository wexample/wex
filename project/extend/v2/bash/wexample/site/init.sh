#!/usr/bin/env bash

siteInitArgs() {
  _ARGUMENTS=(
    [0]='services s "Services to install" true',
    [1]='site_name n "Site name" false',
    [2]='git g "Init git repository" false',
    [3]='environment e "Environment (local default)" false'
    [4]='domains d "Domains names separated by a comma" false'
  )
}

siteInit() {
  local RENDER_BAR='wex render/progressBar -w=30 '
  # Status
  ${RENDER_BAR} -p=0 -s="Init variables"

  local DIR_SITE=./

  if [ -z "${GIT+x}" ]; then
    GIT=true
  fi;

  if [ -z "${ENVIRONMENT+x}" ]; then
    ENVIRONMENT=local
  fi;

  # Default site name.
  if [[ -z "${SITE_NAME+x}" ]]; then
    # Name is current dir name.
    local SITE_NAME="$(basename $( realpath "${DIR_SITE}" ))"
  fi;

  # Do not allow underscore in site name :
  # site name may be used for local domain name,
  # which not support underscore.
  NAME=$(wex text/camelCase -t=${SITE_NAME})

  local SITE_DIR_DOCKER=${DIR_SITE}"docker/"
  local WEX_DIR_DOCKER_SERVICES=${WEX_DIR_ROOT}"services/"

  # Split services
  local SERVICES_JOINED=$(wex service/tree -s="${SERVICES}")
  local SERVICES=$(echo ${SERVICES_JOINED} | tr "," "\n")

  # Check services exists
  for SERVICE in ${SERVICES[@]}
  do
    if [ ! -d ${WEX_DIR_DOCKER_SERVICES}${SERVICE} ];then
      echo -e "\nError : Service missing "${SERVICE}
      exit
    fi
  done

  # Status
  ${RENDER_BAR} -p=10 -s="Copy base samples files"

  local SAMPLE_SITE_DIR=${WEX_DIR_SAMPLES}site/
  # Copy base site files.
  cp -n -R ${SAMPLE_SITE_DIR}. ${DIR_SITE}

  # Creating default env file
  if [ ! -f ".env" ]; then
    echo -e "SITE_ENV="${ENVIRONMENT} > .env
  fi

  local WEX_VERSION=$(wex wex/version)

  # Create wex file early to enable wexample namespace.
  touch .wex
  # Create wex file
  cat <<EOF > .wex
# Global
AUTHOR=$(whoami)
CREATED="$(date -u)"
IMAGES_VERSION=latest
NAME=${SITE_NAME}
SERVICES=${SERVICES_JOINED}
WEX_VERSION=${WEX_VERSION}

# Local
LOCAL_DOMAIN_MAIN=${SITE_NAME}.wex
LOCAL_DOMAINS=${SITE_NAME}.wex
EOF

  if [ "${DOMAINS}" != "" ];then
    local DOMAINS_SPLIT=$(wex text/split -t=${DOMAINS} -s=",")
    local DOMAINS_MAIN=${DOMAINS_SPLIT[0]}
  else
    local DOMAINS=domain.com
    local DOMAINS_MAIN=domain.com
  fi

  cat <<EOF >> .wex

# Prod
PROD_DOMAIN_MAIN=${DOMAINS_MAIN}
PROD_DOMAINS=${DOMAINS}
PROD_EMAIL=contact@${DOMAINS_MAIN}
EOF

  mkdir -p docker

  local NEW_SITE_NAME=${SITE_NAME}

  # Default project dir
  if [ ! -d project ]; then
    # Creating default dir
    mkdir project
    echo -e ${SITE_NAME}"\n===" > project/README.txt
  fi;

  for SERVICE in ${SERVICES[@]}
  do
     # Status
    ${RENDER_BAR} -p=20 -s="Installing service "${SERVICE}
    wex service/install -s=${SERVICE} -g=${GIT}
  done

  # GIT Common settings
  ${RENDER_BAR} -p=30 -s="Init GIT repo"
  # Already exist
  if [ -f ${DIR_SITE}".gitignore" ]; then
    # Merge ignore file
    cat ${DIR_SITE}.gitignore.source >> ${DIR_SITE}.gitignore
    rm ${DIR_SITE}.gitignore.source
  else
    mv ${DIR_SITE}.gitignore.source ${DIR_SITE}.gitignore
  fi
  # Create CI file.
  wex gitlab/init

  # Init GIT repo
  if [ "${GIT}" == true ];then
    # Status
    ${RENDER_BAR} -p=50 -s="Install GIT" -nl
    # Create a GIT repo if not exists.
    git init
  fi

  # Status
  ${RENDER_BAR} -p=80 -s="Init services" -nl

  wex config/write

  # Init
  wex hook/exec -c=init

  # Status
  ${RENDER_BAR} -p=100 -s="Done !" -nl

  if [ ${NEW_SITE_NAME} != ${WEX_WEXAMPLE_PROXY_CONTAINER}_prod ];then
    _wexMessage "Your site is initialized as ${NEW_SITE_NAME}" "You may start install process using :" "wex site/install"
  fi
}
