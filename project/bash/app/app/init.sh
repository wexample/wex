#!/usr/bin/env bash

appInitArgs() {
  _ARGUMENTS=(
     'services s "Services to install" true',
     'site_name n "Site name" false',
     'git g "Init git repository" false true',
     'environment e "Environment (local default)" false local'
     'domains d "Domains names separated by a comma" false'
  )
}

appInit() {
  local RENDER_BAR='wex prompt/progress -nl '
  # Status
  ${RENDER_BAR} -p=0 -s="Init variables"

  local DIR_SITE=./

  # Default site name.
  if [ "${SITE_NAME}" = "" ]; then
    # Name is current dir name.
    SITE_NAME="$(basename "$(realpath "${DIR_SITE}")")"
  fi;

  # Do not allow underscore in site name :
  # site name may be used for local domain name,
  # which not support underscore.
  local NAME
  NAME=$(echo "${SITE_NAME}" | tr '_' '-')

  _wexLog "Using name ${NAME}"

  local SITE_DIR_DOCKER=${DIR_SITE}"docker/"
  local WEX_DIR_DOCKER_SERVICES=${WEX_DIR_ROOT}"services/"

  # Create wex file early to enable wexample namespace.

  # Split services
  local SERVICES_JOINED=$(wex app::service/tree -s="${SERVICES}")
  local SERVICES=$(echo "${SERVICES_JOINED}" | tr "," "\n")

  # Check services exists
  for SERVICE in ${SERVICES[@]}
  do
    if [ ! -d "${WEX_DIR_DOCKER_SERVICES}${SERVICE}" ];then
      _wexError "Service missing ${SERVICE}"
      rm .wex
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

  local WEX_VERSION
  WEX_VERSION=$(wex core/version)

  # Create wex file
  cat <<EOF > .wex
NAME=${SITE_NAME}
AUTHOR=$(whoami)
CREATED="$(date -u)"
IMAGES_VERSION=latest
SERVICES=${SERVICES_JOINED}
LOCAL_DOMAINS=${SITE_NAME}.wex
LOCAL_DOMAIN_MAIN=${SITE_NAME}.wex
WEX_VERSION=${WEX_VERSION}
EOF

  if [ "${DOMAINS}" != "" ];then
    local DOMAINS_SPLIT=$(wex string/split -t="${DOMAINS}" -s=",")
    local DOMAINS_MAIN=${DOMAINS_SPLIT[0]}
  else
    local DOMAINS=domain.com
    local DOMAINS_MAIN=domain.com
  fi

  {
    echo "PROD_DOMAINS=${DOMAINS}"
    echo "PROD_DOMAIN_MAIN=${DOMAINS_MAIN}"
    echo "PROD_EMAIL=contact@${DOMAINS_MAIN}"
  } >> .wex

  mkdir -p docker

  local NEW_SITE_NAME=${SITE_NAME}

  # Default project dir
  if [ ! -d project ]; then
    # Creating default dir
    mkdir project
    echo -e "#${SITE_NAME}" > project/README.txt
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

  # Init GIT repo
  if [ "${GIT}" = true ];then
    # Status
    ${RENDER_BAR} -p=50 -s="Install GIT"
    # Create a GIT repo if not exists.
    git init
  fi

  # Status
  ${RENDER_BAR} -p=80 -s="Init services"

  wex config/write

  # Init
  wex hook/exec -c=init

  # Status
  ${RENDER_BAR} -p=100 -s="Done !"

  if [ "${NEW_SITE_NAME}" != "${WEX_PROXY_CONTAINER}" ];then
    _wexMessage "Your site is initialized as ${NEW_SITE_NAME}" "You may start install process using :" "wex app/install"
  fi
}
