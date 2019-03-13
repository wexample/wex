#!/usr/bin/env bash

symfony4DbMigrate() {
  wex site/exec -l -c="php bin/console doctrine:migrations:migrate"
}