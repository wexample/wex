#!/usr/bin/env bash

moodleStarted() {
    # Same config as web
  . ${WEX_DIR_ROOT}services/web/started.sh

  webStarted

  # Give access.
  wex site/exec -c="chmod 755 /var/www/html/moodledata"
  wex site/exec -c="chown www-data:www-data /var/www/html/moodledata"
}