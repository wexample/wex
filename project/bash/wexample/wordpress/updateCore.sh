#!/usr/bin/env bash

wordpressUpdateCoreArgs() {
  _DESCRIPTION="Udpate WP core file when wp-cli does not do the job. Let user to update database from admin."
  _ARGUMENTS=(
    [0]='version v "Wordpress version number (ex: 4.9.5)" true'
  )
}

wordpressUpdateCore() {
  local FILENAME='wordpress-'${VERSION}'.zip'
  # Download last version.
  wex site/exec -c="cd /var/www && wget https://wordpress.org/${FILENAME} && unzip ${FILENAME} && rm ${FILENAME}"
  # Remove old files.
  wex site/exec -c="rm -rf /var/www/html/project/wp-includes && rm -rf /var/www/html/project/wp-admin"
  # Copy new
  wex site/exec -c="cp -r /var/www/wordpress/wp-includes /var/www/html/project"
  wex site/exec -c="cp -r /var/www/wordpress/wp-admin /var/www/html/project"
  # Copy without removing existing.
  wex site/exec -c="cp -r /var/www/wordpress/wp-content /var/www/html/project"
  # Copy root files
  wex site/exec -c="cp /var/www/wordpress/* /var/www/html/project"
  # Now user should visit wp-admin for database migration.
}