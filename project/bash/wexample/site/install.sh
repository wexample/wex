#!/usr/bin/env bash

siteInstall() {
  if [ $(wex site/isset) ];then
    # Add proper rights.
    wex site/exec -c="chown -R www-data:www-data /var/www/html/project"
    # Call services hooks.
    wex service/exec -c=install
    # Execute framework scripts.
    wex framework/exec -c=install
    # Call local ci hooks.
    wex ci/exec -c=install
  fi
}