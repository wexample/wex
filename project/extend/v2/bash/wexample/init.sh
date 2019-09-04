#!/usr/bin/env bash

export WEX_WEXAMPLE_DIR_TMP=${WEX_DIR_TMP}wexample/
export WEX_WEXAMPLE_DIR_DATA=${WEX_DIR_ROOT_REPO}data/
# /opt can't be mounted on macos, using Users instead.
export WEX_WEXAMPLE_DIR_PROXY=$([[ "$(uname -s)" == Darwin ]] && echo /Users/.wex/server/ || echo /opt/wex_server/)
export WEX_WEXAMPLE_DIR_PROXY_TMP=${WEX_WEXAMPLE_DIR_PROXY}tmp/
export WEX_WEXAMPLE_DIR_MAIL_TMP=${WEX_WEXAMPLE_DIR_TMP}mail/
export WEX_WEXAMPLE_PROXY_CONTAINER=wex_server
export WEX_WEXAMPLE_DIR_SITES_DEFAULT=/var/www/
export WEX_WEXAMPLE_SITE_DIR_TMP=./tmp/
export WEX_WEXAMPLE_SITE_CONFIG=${WEX_WEXAMPLE_SITE_DIR_TMP}config
export WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML=${WEX_WEXAMPLE_SITE_DIR_TMP}docker-compose.build.yml
export WEX_WEXAMPLE_ENVIRONMENTS=(local dev prod)
export WEX_GITLAB_URL=gitlab.wexample.com
export WEXAMPLE_SITE_LOCAL_VAR_STORAGE=${WEX_WEXAMPLE_SITE_DIR_TMP}variablesLocalStorage

wexampleSiteInitLocalVariables() {
  if [[ ! -f ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE} ]];then
    touch ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE};
  fi
}
