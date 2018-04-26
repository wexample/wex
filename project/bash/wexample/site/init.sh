#!/usr/bin/env bash

siteInitArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false',
    [1]='services s "Services to install" false',
    [2]='name n "Site name" false',
    [3]='git g "Init git repository" false',
    [4]='environment e "Environment (local default)" false',
  )
}

siteInit() {

  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  if [ -z "${GIT+x}" ]; then
    GIT=true
  fi;

  if [ -z "${ENVIRONMENT+x}" ]; then
    ENVIRONMENT=local
  fi;

  # Default services.
  if [[ -z "${SERVICES+x}" ]]; then
    SERVICES=("web")
  fi;

  # TODO Exit if any service does not exists.
  # TODO Do not init already existing services
  # TODO Allow to remove services
  # TODO If no service defined, ask user for each one
  # TODO Allow per environment services (local.service => watcher)

  # Default services.
  if [[ -z "${NAME+x}" ]]; then
    # Name is current dir name.
    local NAME="$(basename $( realpath "${DIR_SITE}" ))"
  fi;

  # Do not allow underscore in site name :
  # site name may be used for local domain name,
  # which not support underscore.
  NAME=$(wex text/camelCase -t=${NAME})

  # Copy site files.
  cp -n -R ${WEX_DIR_SAMPLES}site/. ${DIR_SITE}

  # Creating default env file
  if [ ! -f ".env" ]; then
    echo -e "SITE_ENV="${ENVIRONMENT} > .env
  fi

  if [ ! -f ".wex" ]; then
    cat <<EOF > .wex
NAME=${NAME}
AUTHOR=$(whoami)
CREATED="$(date -u)"
SERVICES=${SERVICES}
EOF
  fi;

  # Default project dir
  if [ ! -d project ]; then
    # Creating default dir
    mkdir project
    echo -e ${NAME}"\n===" > project/README.txt
  fi;

  if [ ${GIT} == true ];then
    # Already exist
    if [ -f ${DIR_SITE}".gitignore" ]; then
      # Merge ignore file
      cat ${DIR_SITE}.gitignore.source >> ${DIR_SITE}.gitignore
      rm ${DIR_SITE}.gitignore.source
    else
      mv ${DIR_SITE}.gitignore.source ${DIR_SITE}.gitignore
    fi
  fi

  # Split services
  SERVICES=($(echo ${SERVICES} | tr "," "\n"))

  SITE_DIR_DOCKER=${DIR_SITE}"docker/"

  YML=$(ls ${SITE_DIR_DOCKER})

  # For each yml type file.
  for YML_FILE in ${YML[@]}
  do

    YML_TO_ADD=""
    # For each service.
    for SERVICE in ${SERVICES[@]}
    do
      SERVICE_DIR_SITE=${WEX_DIR_SAMPLES}"services/"${SERVICE}"/"
      SERVICE_YML_FILE=${SERVICE_DIR_SITE}"docker/"${YML_FILE}

      if [[ -f ${SERVICE_YML_FILE} ]];then
        YML_TO_ADD+="\n    "${SERVICE}":"
        YML_TO_ADD+="\n"$(cat ${SERVICE_YML_FILE})
      fi
    done;

    if [[ ${YML_TO_ADD} ]];then
      YML_DEST=${DIR_SITE}"docker/"${YML_FILE}
      YML_SOURCE=$(cat ${YML_DEST})
      YML_FINAL=""

      # Search for placeholder, respecting line breaks.
      # TODO When init is launched on an existing yml file
      #  1/ We loose line breaks and tabs
      #  2/ We not have #[SERVICES] placeholder
      # > We may work on a special test case to add / remove services on existing yml file
      while read LINE; do
        # Trim
        if [[ $(echo -e "${LINE}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') == "#[SERVICES]" ]];then
          YML_FINAL+="${YML_TO_ADD}"
        else
          YML_FINAL+="\n${LINE}"
        fi;
      done <${YML_DEST}

      echo -e "${YML_FINAL}" > ${YML_DEST}
    fi
  done;

  for SERVICE in ${SERVICES[@]}
  do
    SERVICE_DIR_SITE=${WEX_DIR_SAMPLES}"services/"${SERVICE}"/"

    # There is a site folder in service.
    # And not in the dest site.
    if [[ -d ${SERVICE_DIR_SITE} ]] && [[ ! -d ${DIR_SITE}${SERVICE} ]];then
      cp -n -R $(realpath ${SERVICE_DIR_SITE})/. $(realpath ${DIR_SITE})
    fi

    # Merge ignore file
    if [ ${GIT} == true ] && [[ -f ${DIR_SITE}.gitignore.source ]];then
      cat ${DIR_SITE}.gitignore.source >> ${DIR_SITE}".gitignore"
      rm ${DIR_SITE}.gitignore.source
    fi
  done;

  if [ ${GIT} == true ];then
    # Create a GIT repo if not exists.
    git init
    # Init git hooks.
    wex git/initHooks
    # Create CI file.
    wex gitlab/init
  fi

  wex service/exec -c="init"
}
