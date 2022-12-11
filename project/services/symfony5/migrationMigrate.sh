#!/usr/bin/env bash

symfony5MigrationMigrate() {
  # Clearing cache in production is important
  # for container aware migrations.
  wex cache/clear

  wex site/exec -l -c="php bin/console doctrine:migrations:migrate"
}