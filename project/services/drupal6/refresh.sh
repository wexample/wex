#!/usr/bin/env bash

drupal6Refresh() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/refresh.sh

  webRefresh
}