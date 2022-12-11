#!/usr/bin/env bash

symfony4AppConfig() {
  # Same as web
  . ${WEX_DIR_SERVICES}web/hooks/appConfig.sh

  webAppConfig

  wex config/setValue -k=SITE_CONTAINER -v=symfony4
}
