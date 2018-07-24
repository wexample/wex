#!/usr/bin/env bash

frameworkComposer1Update() {
  # Execute composer command as www-data user.
  su - www-data -s /bin/bash -c 'cd /var/www/html/project && composer install'
}
