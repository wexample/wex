#!/usr/bin/env bash

# Go to repo.
cd /var/www/html

# Get last updates.
git pull
# Update packages.
composer install

# Update database
php bin/console doctrine:database:create --env=prod --if-not-exists
php bin/console doctrine:schema:create --env=prod

# Update Yarn
yarn updateYarn
# Build files
yarn buildAppFiles

cd web

# Clear cache
rm -rf var/cache
# Clear wexample cache
php bin\console cache_clear
# Rebuild minimum cache
php bin/console cache:warmup

# Give user writes
chown -R www-data:www-data *
