#!/usr/bin/env bash

service apache2 restart

cd /var/www/html

# Update project.
composer clear-cache -q
composer update -q

/bin/bash
