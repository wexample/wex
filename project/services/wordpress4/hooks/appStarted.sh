#!/usr/bin/env bash

wordpress4AppStarted() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appStarted.sh

  webAppStarted

  . .wex

  # There is a different core version.
  if [ "${WP_CORE_VERSION}" != "" ] && [ "${WP_CORE_VERSION}" != "$(wex wordpress/version)" ];then
    _wexLog "Upgrading wordpress core to ${WP_CORE_VERSION}"
    # Update core.
    wex wordpress/changeCore -v="${WP_CORE_VERSION}"
  fi

  echo "WP_CORE_VERSION=${WP_CORE_VERSION}" >> .wex
}