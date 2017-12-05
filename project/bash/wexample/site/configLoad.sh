#!/usr/bin/env bash

siteConfigLoadArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
  )
}

siteConfigLoad() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Load config
  wexLog "Loading site config file"
  CONFIG=$(cat ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG})
  # Export each variable for yml files.
  for LINE in ${CONFIG[@]};do
    if [[ ${LINE} ]];then
      export ${LINE}
    fi
  done

  wexLog "Getting domains"
  # Global variables
  export DOMAINS=$(wex site/domains -d=${DIR_SITE})

  wexLog "Exporting site variables"

  export WEX_SCRIPTS_PATH=${WEX_DIR_ROOT}
  export SITE_PATH_ROOT=$(realpath ${DIR_SITE})"/"

  # Get framework specific settings.
  wex framework/settings -d=${DIR_SITE}"project"

  # Expose settings.
  export SITE_DB_HOST=${SITE_DB_HOST}
  export SITE_DB_NAME=${SITE_DB_NAME}
  export SITE_DB_USER=${SITE_DB_USER}
  export SITE_DB_PASSWORD=${SITE_DB_PASSWORD}
}
