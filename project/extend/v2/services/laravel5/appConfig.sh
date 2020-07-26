#!/usr/bin/env bash

laravel5AppConfig() {
  # Same as web
  . ${WEX_DIR_SERVICES}web/appConfig.sh

  webAppConfig

  # Override default container.
  echo -e "\nSITE_CONTAINER=laravel5" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
