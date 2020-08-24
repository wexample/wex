#!/usr/bin/env bash

export WEX_WEXAMPLE_DIR_DATA=${WEX_DIR_ROOT_REPO}data/
# /opt can't be mounted on macos, using Users instead.
export WEX_WEXAMPLE_DIR_PROXY=$([[ "$(uname -s)" == Darwin ]] && echo /Users/.wex/server/ || echo /opt/wex_server/)
export WEX_DIR_PROXY_TMP=${WEX_WEXAMPLE_DIR_PROXY}tmp/
export WEX_WEXAMPLE_DIR_SITES_DEFAULT=/var/www/
export WEX_WEXAMPLE_SITE_DIR_TMP=./tmp/
export WEX_APP_COMPOSE_BUILD_YML=${WEX_WEXAMPLE_SITE_DIR_TMP}docker-compose.build.yml
export WEX_GITLAB_URL=gitlab.wexample.com
export WEXAMPLE_SITE_LOCAL_VAR_STORAGE=${WEX_WEXAMPLE_SITE_DIR_TMP}variablesLocalStorage

wexampleSiteInitLocalVariables() {
  if [[ ! -f ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE} ]];then
    touch ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE};
  fi
}

# User should be sudo or member to the "docker" group.
# Prevent to check twice.
if [ -z ${WEX_DOCKER_USER_RIGHTS_VERIFIED} ];then
  WEX_DOCKER_USER_RIGHTS_VERIFIED=true

  # User is not sudo
  if [[ ${EUID} > 0 ]];then
    # User should have right to run Docker
    WEX_USERNAME=$(whoami)
    WEX_GROUP=docker

    if [[ ! $(id -nG "${WEX_USERNAME}" | grep -c "${WEX_GROUP}") ]]; then
      WEX_DOCKER_USER_RIGHTS_VERIFIED=false
      _wexError "${WEX_USERNAME} does not belong to \"${WEX_GROUP}\" and is not sudo" "You may fix it with : sudo usermod -a -G ${WEX_GROUP} ${WEX_USERNAME}" "! Don't forget to restart your machine to make changes takes effect !"
    fi
  fi

  export WEX_DOCKER_USER_RIGHTS_VERIFIED
fi
