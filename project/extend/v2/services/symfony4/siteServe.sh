#!/usr/bin/env bash

symfony4SiteServe() {
  # Same as web
  . ${WEX_DIR_SERVICES}web/siteServe.sh

  webSiteServe
}