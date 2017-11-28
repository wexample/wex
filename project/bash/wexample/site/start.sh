#!/usr/bin/env bash

siteStart() {
  # Server must be started.
  wex server/start -n

  if [[ $(wex site/started) == false ]];then
    # Write new config
    wex site/configWrite -s
    # Add site
    wex server/siteStart -d="./"
    # Docker compose
    wex site/compose -c="up -d --build"
    # Show domains.
    echo $(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts)
  fi;
}
