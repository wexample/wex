#!/usr/bin/env bash

drupal7Refresh() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/refresh.sh

  webRefresh
}