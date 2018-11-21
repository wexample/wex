#!/usr/bin/env bash

frameworkComposer1Update() {
  # TODO Agnostic path
  # Access must be given to www-data
  # Execute composer command as www-data user.
  su - www-data -s /bin/bash -c 'cd /var/www/html/project/ && composer install'
}
