#!/usr/bin/env bash

wordpress4Config() {
  # Same config as web
  . ${WEX_DIR_ROOT}services/web/config.sh

  webConfig

  # Override default container.
  echo "\nSITE_CONTAINER=wordpress4"
}
