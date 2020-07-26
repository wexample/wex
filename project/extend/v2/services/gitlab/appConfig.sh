#!/usr/bin/env bash

gitlabAppConfig() {
  . .wex
  # Override default container.
  echo -e "\nSITE_CONTAINER=gitlab" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nGITLAB_VERSION="${GITLAB_VERSION}
}
