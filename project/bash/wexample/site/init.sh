#!/usr/bin/env bash

siteInitArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false',
    [1]='services s "Services to install" false',
  )
}

siteInit() {

  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Default services.
  if [[ -z "${SERVICES+x}" ]]; then
    SERVICES=("web")
  fi;

  # Name is current dir name.
  local NAME="$(basename $( realpath "${DIR_SITE}" ))"
  # Do not allow underscore in site name :
  # site name may be used for local domain name,
  # which not support underscore.
  NAME=$(wex text/camelCase -t=${NAME})

  # Copy site files.
  cp -n -R ${WEX_DIR_ROOT}samples/site/. ${DIR_SITE}

  # Creating default env file
  if [ ! -f ".env" ]; then
    wexLog "Creating .env file"
    echo -e "SITE_ENV=local" > .env
  fi

  if [ ! -f "wex.json" ]; then
    wexLog "Creating wex.json"
    cat <<EOF > wex.json
{
  "name": "${NAME}",
  "author": "$(whoami)",
  "created": "$(date -u)",
  "services": "${SERVICES}"
}
EOF
  fi;

  # Default project dir
  if [ ! -d project ]; then
    wexLog "Creating project folder"
    # Creating default dir
    mkdir project
    echo -e ${NAME}"\n===" > project/README.txt
  fi;

  # Already exist
  if [ -f ${DIR_SITE}".gitignore" ]; then
    wexLog "Merging gitignore"
    # Merge ignore file
    cat ${DIR_SITE}.gitignore.source >> ${DIR_SITE}.gitignore
    rm ${DIR_SITE}.gitignore.source
  else
    wexLog "Moving gitignore"
    mv ${DIR_SITE}.gitignore.source ${DIR_SITE}.gitignore
  fi;

  # Split services
  SERVICES=($(echo ${SERVICES} | tr "," "\n"))

  SITE_DIR_DOCKER=${DIR_SITE}"docker/"

  YML=$(ls ${SITE_DIR_DOCKER})

  # For each yml type file.
  wexLog "Append YML content"
  for YML_FILE in ${YML[@]}
  do
    wexLog "  Installing "${YML_FILE}

    YML_TO_ADD=""
    # For each service.
    for SERVICE in ${SERVICES[@]}
    do
      SERVICE_DIR=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/"
      SERVICE_DIR_SITE=${SERVICE_DIR}"site/"
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

      wexLog "    Append YML content to "${YML_DEST}

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

  wexLog "Installing services"
  for SERVICE in ${SERVICES[@]}
  do
    SERVICE_DIR=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/"
    SERVICE_DIR_SITE=${SERVICE_DIR}"site/"

    wexLog "  "${SERVICE}

    # There is a site folder in service.
    # And not in the dest site.
    if [[ -d ${SERVICE_DIR_SITE} ]] && [[ ! -d ${DIR_SITE}${SERVICE} ]];then
      cp -n -R $(realpath ${SERVICE_DIR_SITE})/. $(realpath ${DIR_SITE})
    fi

    # Merge ignore file
    if [[ -f ${DIR_SITE}.gitignore.source ]];then
      cat ${DIR_SITE}.gitignore.source >> ${DIR_SITE}".gitignore"
      rm ${DIR_SITE}.gitignore.source
    fi
  done;

  # Init git hooks.
  wex git/initHooks

  wex service/exec -c="init"

  # Create CI file.
  wex gitlab/init
}
