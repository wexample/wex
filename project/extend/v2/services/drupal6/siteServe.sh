#!/usr/bin/env bash

drupal6SiteServe() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/siteServe.sh

  webSiteServe
}