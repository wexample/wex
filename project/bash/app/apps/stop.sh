#!/usr/bin/env bash

appsStop() {
  if [ ! -f "${WEX_PROXY_APPS_REGISTRY}" ];then
    return
  fi

  REGISTRY=$(cat "${WEX_PROXY_APPS_REGISTRY}")

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [ "$(wex string/trim -s=${SITE_PATH})" != "" ];then
      # Keep wex_server alive.
      if [ "$(basename "${SITE_PATH}")" != 'wex_server' ];then
        cd "${SITE_PATH}"
        wex app/stop
      fi
    fi
  done;
}
