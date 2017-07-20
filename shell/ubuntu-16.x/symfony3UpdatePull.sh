#!/usr/bin/env bash

# Make a pull on a production symfony 3.x
# It may be executed remotely by a CI tool when unit test has been complete

#TODO Use variable repo name

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
yarn install
cd web
yarn install
cd ../

# Clear cache
rm -rf var/cache
# Clear wexample cache
php bin\console cache_clear
# Rebuild minimum cache
php bin/console cache:warmup

# Give user writes
chown -R www-data:www-data *
