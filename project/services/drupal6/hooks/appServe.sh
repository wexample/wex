#!/usr/bin/env bash

drupal6AppServe() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appServe.sh

  webAppServe
}