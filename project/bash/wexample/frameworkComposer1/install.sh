#!/usr/bin/env bash

frameworkComposer1Install() {
  # Install composer.
  wex site/exec -c="cd /var/www/html/project/ && wex frameworkComposer1/update"
}
