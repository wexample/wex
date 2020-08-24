#!/usr/bin/env bash

drupal6AppConfig() {
  # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appConfig.sh

  webAppConfig

  # Override default container.
  echo -e "\nSITE_CONTAINER=drupal6" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
