#!/usr/bin/env bash

sonarqubeAppConfig() {
  . .wex

  # Set the used version
  echo -e "\nSONARQUBE_VERSION=${SONARQUBE_VERSION}" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  # Override default container.
  echo -e "\nSITE_CONTAINER=sonarqube" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}