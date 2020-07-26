#!/usr/bin/env bash

drupal7Config() {
  # Same config as web
  . ${WEX_DIR_SERVICES}web/appConfig.sh

  webAppConfig

  # Override default container.
  echo -e "\nSITE_CONTAINER=drupal7" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
