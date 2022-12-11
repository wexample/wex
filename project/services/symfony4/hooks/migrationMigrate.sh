#!/usr/bin/env bash

symfony4MigrationMigrate() {
  wex app/exec -l -c="php bin/console doctrine:migrations:migrate"
}