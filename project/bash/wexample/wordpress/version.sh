#!/usr/bin/env bash

wordpressVersion() {
  wex site/exec -c="grep wp_version /var/www/html/project/wp-includes/version.php"
}