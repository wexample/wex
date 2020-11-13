#!/usr/bin/env bash

symfony4MigrationDiff() {
  wex cli/exec -c="doctrine:migration:diff"
}