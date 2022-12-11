#!/usr/bin/env bash

laravel5SiteServe() {
  # Same as web
  . ${WEX_DIR_SERVICES}web/hooks/appServe.sh

  webAppServe
}