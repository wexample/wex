#!/usr/bin/env bash

nodeAppConfig() {
  # Nginx conf
  wex config/bindFiles -s=nginx -e=conf

  echo -e "\nSITE_CONTAINER=node" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
