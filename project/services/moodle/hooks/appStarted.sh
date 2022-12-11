#!/usr/bin/env bash

moodleAppStarted() {
    # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appStarted.sh

  webAppStarted

  # Give access.
  wex app/exec -c="chmod -R 755 /var/www/html/moodledata"
  wex app/exec -c="chown -R www-data:www-data /var/www/html/moodledata"
}