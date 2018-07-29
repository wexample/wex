#!/usr/bin/env bash

wordpress4Refresh() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/refresh.sh

  webRefresh
}