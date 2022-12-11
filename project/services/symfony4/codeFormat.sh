#!/usr/bin/env bash

symfony4CodeFormat() {
    # Same as web
  . ${WEX_DIR_ROOT}services/web/codeFormat.sh

  webCodeFormat
}