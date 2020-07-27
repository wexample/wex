#!/usr/bin/env bash

drupal7Started() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/started.sh

  webStarted

  # Give access.
  wex site/exec -c="chmod -R 777 /var/www/html/project/sites/default/files"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/sites/default/files"
}