#!/usr/bin/env bash

symfony4AppServe() {
  # Same as web
  . ${WEX_DIR_SERVICES}web/hooks/appServe.sh

  webAppServe
}