#!/usr/bin/env bash

drupal7AppStarted() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/started.sh

  webAppStarted

  # Give access.
  wex app/exec -c="chmod -R 777 /var/www/html/project/sites/default/files"
  wex app/exec -c="chown -R www-data:www-data /var/www/html/project/sites/default/files"
}