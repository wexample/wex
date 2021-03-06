#!/usr/bin/env bash

wordpress4Started() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted

  . .wex

  # There is a different core version.
  if [ "${WP_CORE_VERSION}" != "" ] && [ "${WP_CORE_VERSION}" != "$(wex wordpress/version)" ];then
    _wexLog "Upgrading wordpress core to ${WP_CORE_VERSION}"
    # Update core.
    wex wordpress/changeCore -v="${WP_CORE_VERSION}"
  fi

  wex config/changeValue -f=.wex -k=WP_CORE_VERSION -v="${WP_CORE_VERSION}" -s
}