#!/usr/bin/env bash

moodleAppConfig() {
  . ${WEX_DIR_SERVICES}web/appConfig.sh
  webAppConfig

  # Override default container.
  echo -e "\nSITE_CONTAINER=moodle" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}