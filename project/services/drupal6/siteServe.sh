#!/usr/bin/env bash

drupal6SiteServe() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/siteServe.sh

  siteServe
}