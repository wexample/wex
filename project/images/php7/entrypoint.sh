#!/usr/bin/env bash

# Load parent entry point.
bash /docker-entrypoint-webserver.sh

# Update project.
composer clear-cache -q
composer update -q

cd /var/www/html

