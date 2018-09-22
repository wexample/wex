#!/usr/bin/env bash

frameworkComposer1Update() {
  # TODO Agnostic path
  # Files access
  chown www-data:www-data /var/www/html/project/composer.lock
  chown -R www-data:www-data /var/www/html/project/vendor
  # Execute composer command as www-data user.
  su - www-data -s /bin/bash -c 'cd /var/www/html/project/ && composer install'
}
