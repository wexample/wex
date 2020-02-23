#!/usr/bin/env bash

symfony4MigrationCreate() {
  wex cli/exec -c="doctrine:migration:generate"
}