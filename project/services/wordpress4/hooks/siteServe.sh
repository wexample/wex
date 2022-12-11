#!/usr/bin/env bash

wordpress4SiteServe() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appServe.sh

  webAppServe
}