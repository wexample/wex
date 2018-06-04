#!/usr/bin/env bash

frameworkComposer1Pull() {
  wex site/exec -c="cd /var/www/html/project/ && composer update -d=./project/"
}
