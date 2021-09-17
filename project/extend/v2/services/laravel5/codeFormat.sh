#!/usr/bin/env bash

laravel5CodeFormat() {
    # Same as web
  . ${WEX_DIR_ROOT}services/web/codeFormat.sh

  webCodeFormat
}