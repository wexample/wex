#!/usr/bin/env bash

symfony4MigrationMigrate() {
  wex site/exec -l -c="php bin/console doctrine:migrations:migrate"
}