#!/usr/bin/env bash

wordpress4Perms() {
  # Allow rewriting by app itself.
  wex site/exec -l -c="chown www-data:www-data .htaccess"
  wex site/exec -l -c="chmod 755 .htaccess"
}