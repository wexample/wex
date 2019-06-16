#!/usr/bin/env bash

wordpress4Started() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted
}