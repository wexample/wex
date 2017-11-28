#!/usr/bin/env bash

# TODO replace by sites/stopAll
# TODO Error ERROR: yaml.scanner.ScannerError: mapping values are not allowed here in ".\docker/docker-compose.yml", line 17, column 37
serverStopSites() {
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  for SITE_PATH in ${REGISTRY[@]}
  do
    # Avoid blank lines.
    if [[ $(wex text/trim -t=${SITE_PATH}) != "" ]];then
      cd ${SITE_PATH}
      wex site/stop
    fi
  done;
}
