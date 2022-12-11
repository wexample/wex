#!/usr/bin/env bash

wordpress4Perms() {
  # Allow rewriting by app itself.
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project"
  wex site/exec -c="chmod -R 755 /var/www/html/project"
}