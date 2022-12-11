#!/usr/bin/env bash

siteReinit() {
  if [ ! -f .wex ];then
    # We are not in a wexample site.
    exit
  fi

  # Stop if running.
  wex app/stop

  local GIT=$([ -d .git ] && echo true || echo false)

  # Load conf.
  . ${WEX_APP_CONFIG}
  . .wex

  # Go to parent dir.
  cd ../
  # Remove dir.
  rm -rf ./${SITE_NAME}
  # Create new dir.
  mkdir ${SITE_NAME}
  cd ${SITE_NAME}

  wex site/init -s=${SERVICES} -g=${GIT}
}