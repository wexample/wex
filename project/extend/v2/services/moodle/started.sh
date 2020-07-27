#!/usr/bin/env bash

moodleStarted() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/started.sh

  webStarted

  # Give access.
  wex site/exec -c="chmod -R 755 /var/www/html/moodledata"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/moodledata"
}