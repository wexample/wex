#!/usr/bin/env bash

wordpress4AppStarted() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/started.sh

  webAppStarted

  . .wex

  # There is a different core version.
  if [ "${WP_CORE_VERSION}" != "" ] && [ "${WP_CORE_VERSION}" != $(wex wordpress/version) ];then
    # Update core.
    wex wordpress/changeCore -v=${WP_CORE_VERSION}
  fi

  echo "WP_CORE_VERSION=4.9.5" >> .wex
}