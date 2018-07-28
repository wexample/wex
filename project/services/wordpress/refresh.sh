#!/usr/bin/env bash

wordpressRefresh() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/refresh.sh

  webRefresh
}