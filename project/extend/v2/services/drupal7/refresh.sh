#!/usr/bin/env bash

drupal7SiteServe() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/siteServe.sh

  webSiteServe
}