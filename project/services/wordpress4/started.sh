#!/usr/bin/env bash

wordpress4Started() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted

  . .wex

  # There is a different core version.
  if [ "${WP_CORE_VERSION}" != "" ] && [ "${WP_CORE_VERSION}" != $(wex wordpress/version) ];then
    # Update core.
    wex wordpress/changeCore -v=${WP_CORE_VERSION}
  fi
}