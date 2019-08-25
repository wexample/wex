#!/usr/bin/env bash

drupal7SiteServe() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/siteServe.sh

  webSiteServe
}