#!/usr/bin/env bash

wordpressWexifyArgs() {
  #_DESCRIPTION="Convert an external wordpress site to a wex site. Warning ! Make a backup of your site"
  _ARGUMENTS=(
    [0]='from_wp_install f "Path for root of old wordpress installation" true'
    [1]='version v "Wordpress version number (ex: 4.9.5), see wexample/wordpress4 Dockerfile" true'
  )
}

wordpressWexify() {
  . .wex
  local FOLDER_NAME=$(basename ${FROM_WP_INSTALL})
  # Backup wex config file.
  wex site/exec -c="cp /var/www/html/project/wp-config.php /var/www/"
  wex site/exec -c="cp -r /var/www/html/project/wp-content/config /var/www/"
  # Copy site.
  docker cp ${FROM_WP_INSTALL} ${SITE_NAME}_wordpress4:/var/www/
  # Remove completely internal WP site.
  wex site/exec -c="rm -rf /var/www/html/project/*"
  # Override files.
  wex site/exec -c="cp -r /var/www/${FOLDER_NAME}/* /var/www/html/project"
  # Reset config file
  wex site/exec -c="cp /var/www/wp-config.php /var/www/html/project/ && rm /var/www/wp-config.php"
  wex site/exec -c="cp /var/www/config/* /var/www/html/project/wp-content/config && rm /var/www/config"
  # Update files.
  wex wordpress/updateCore -v=${VERSION}
  # Inform user.
  echo "Files updated, go to /wp-admin/ for database update, then restart site"
}