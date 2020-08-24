#!/usr/bin/env bash

frameworkComposer1Install() {
  # Install composer.
  wex app/exec -c="cd /var/www/html/project/ && wex frameworkComposer1/update"
}
