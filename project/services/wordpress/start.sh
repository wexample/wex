#!/usr/bin/env bash

wordpressStart() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/wordpress/start.sh

  wordpressStart
}