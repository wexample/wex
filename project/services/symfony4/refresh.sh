#!/usr/bin/env bash

symfony4Refresh() {
  # Same as web
  . ${WEX_DIR_ROOT}services/web/refresh.sh

  webRefresh
}