#!/usr/bin/env bash

wordpress4SiteServe() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/siteServe.sh

  webSiteServe
}