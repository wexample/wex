#!/usr/bin/env bash

frameworkComposer1Install() {
  # Install composer.
  wex site/exec -c="cd /var/www/html/project/ && wex frameworkComposer1/update"
  # Test if webpack/encore is installed.
  if [ $(wex site/exec -c="wex file/exists -f=/var/www/html/project/node_modules/.bin/encore") == true ];then
    # Build assets.
    wex site/exec -c="cd /var/www/html/project && yarn run encore dev"
  fi
}
