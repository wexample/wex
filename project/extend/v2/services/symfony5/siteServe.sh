#!/usr/bin/env bash

symfony5SiteServe() {
  # Same as web
  . ${WEX_DIR_ROOT}services/web/siteServe.sh

  webSiteServe
}