#!/usr/bin/env bash

frameworkComposer1Pull() {
  wex site/exec -c="chown www-data:www-data /var/www/html/project && cd /var/www/html/project/ && wex frameworkComposer1/update"
}
