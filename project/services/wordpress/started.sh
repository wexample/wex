#!/usr/bin/env bash

wordpressStarted() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/wordpress/started.sh

  wordpressStarted
}