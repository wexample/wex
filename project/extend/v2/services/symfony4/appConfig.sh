#!/usr/bin/env bash

symfony4AppConfig() {
    # TODO Force using v3. Remove after services migration.
  unset -f wex

  # Same as web
  . ${WEX_DIR_SERVICES}web/appConfig.sh

  webAppConfig

  wex config/setValue -k=SITE_CONTAINER -v=symfony4
}
