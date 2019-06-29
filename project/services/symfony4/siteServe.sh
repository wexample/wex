#!/usr/bin/env bash

symfony4SiteServe() {
  # Same as web
  . ${WEX_DIR_ROOT}services/web/siteServe.sh

  webSiteServe
}