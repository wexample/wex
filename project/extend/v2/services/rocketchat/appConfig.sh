#!/usr/bin/env bash

rocketchatAppConfig() {
  . .wex

  echo -e "\nSITE_CONTAINER=rocketchat" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
  echo -e "\nROCKETCHAT_VERSION=${ROCKETCHAT_VERSION}" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
