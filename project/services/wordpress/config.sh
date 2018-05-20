#!/usr/bin/env bash

wordpressConfig() {
  # Same config as web
  . ${WEX_DIR_ROOT}services/web/config.sh

  webConfig
}
