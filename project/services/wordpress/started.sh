#!/usr/bin/env bash

wordpressStarted() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted
}