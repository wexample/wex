#!/usr/bin/env bash

moodleStarted() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted
}