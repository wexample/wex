#!/usr/bin/env bash

symfony5Config() {
  # Same as web
  . ${WEX_DIR_ROOT}services/web/config.sh

  webConfig

  # Override default container.
  echo "\nSITE_CONTAINER=symfony5"
}
