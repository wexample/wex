#!/usr/bin/env bash

wordpress4AppPerms() {
  # Allow rewriting by app itself.
  wex app/exec -c="chown -R www-data:www-data /var/www/html/project"
  wex app/exec -c="chmod -R 755 /var/www/html/project"
}