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
  if [[ $(wex var/empty -v="${SERVICES}") ]]; then
    SERVICES=("web")
  fi;
  # Name is current dir name.
  NAME="$(basename $( realpath "${DIR_SITE}" ))"

  # Add git
  if [ ! -d .git ]; then
    echo "Init git"
    # Add git.
    git init -q
  fi

  # Copy site files.
  wex dir/copy -f=${WEX_DIR_ROOT}samples/site -t=${DIR_SITE}

  # Creating default env file
  if [ ! -f ".env" ]; then
    echo "Creating .env file"
    echo "SITE_ENV=local" > .env
  fi

  if [ ! -f "wex.json" ]; then
    echo "Creating wex.json"
    cat <<EOF > wex.json
{
  "name" : "${NAME}",
  "author" : "$(whoami)",
  "created" : "$(date -u)",
  "services" : "${SERVICES}"
}
EOF
  fi;

  # Default project dir
  if [ ! -d project ]; then
    echo "Creating project folder"
    # Creating default dir
    mkdir project
    echo -e ${NAME}"\n===" > project/README.txt
  fi;

  # Already exist
  if [ -f ${DIR_SITE}".gitignore" ]; then
    # Merge ignore file
    wex file/merge -s=${DIR_SITE}".gitignore.source" -d=${DIR_SITE}".gitignore"
  else
    mv .gitignore.source .gitignore
  fi;

  # Split services
  SERVICES=($(wex text/split -t=${SERVICES} -s=","))

  SITE_DIR_DOCKER=${DIR_SITE}"docker/"

  YML=$(ls ${SITE_DIR_DOCKER})
  # For each yml type file.
  for YML_FILE in ${YML[@]}
  do
    echo "  Installing "${YML_FILE}

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
      YML_SOURCE=$(cat ${DIR_SITE}"docker/"${YML_FILE})
      YML_FINAL=""

      # Search for placeholder, respecting line breaks.
      while read LINE; do
        if [[ $(wex text/trim -t="${LINE}") == "#[SERVICES]" ]];then
          YML_FINAL+="${YML_TO_ADD}"
        else
          YML_FINAL+=${LINE}
        fi;
      done <${DIR_SITE}"docker/"${YML_FILE}

      echo -e "${YML_FINAL}" > ${DIR_SITE}"docker/"${YML_FILE}
    fi
  done;

  for SERVICE in ${SERVICES[@]}
  do
    SERVICE_DIR=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/"
    SERVICE_DIR_SITE=${SERVICE_DIR}"site/"

    echo "  Installing service "${SERVICE}

    # There is a site folder in service.
    # And not in the dest site.
    if [[ -d ${SERVICE_DIR_SITE} ]] && [[ ! -d ${DIR_SITE}${SERVICE} ]];then
      wex dir/copy -f=$(realpath ${SERVICE_DIR_SITE}) -t=$(realpath ${DIR_SITE})
    fi

    # Merge ignore file
    wex file/merge -s=${DIR_SITE}".gitignore.source" -d=${DIR_SITE}".gitignore"

    # Execute init script.
    SERVICE_FILE_INIT=${SERVICE_DIR}"init.sh"
    # File exists.
    if [[ -f ${SERVICE_FILE_INIT} ]];then
      . ${SERVICE_FILE_INIT}
      METHOD=${SERVICE}"Init"
      # Execute init method.
      ${METHOD}
    fi;
  done;

  # It will recreate config file
  wex site/info
}
