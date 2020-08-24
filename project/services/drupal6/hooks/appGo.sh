#!/usr/bin/env bash

drupal6AppGo() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appGo.sh

  webAppGo
}