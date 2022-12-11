#!/usr/bin/env bash

# This script should be execute on the server hosting the website.
frameworkSymfony3Deploy() {
  deployDir=${1}
  deployEnv="prod"

  # Go to repo.
  cd ${deployDir}

  # Get last updates.
  git pull
  # Update packages.
  composer install

  # Update database
  php bin/console doctrine:database:create --env=${deployEnv} --if-not-exists
  php bin/console doctrine:schema:create --env=${deployEnv}

  # Update Yarn
  yarn updateYarn
  # Build files
  yarn buildAppFiles

  cd web

  # Clear cache
  rm -rf var/cache
  # Rebuild minimum cache
  php bin/console cache:warmup

  # Give user writes
  chown -R www-data:www-data *
}
