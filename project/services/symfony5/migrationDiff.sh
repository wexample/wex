#!/usr/bin/env bash

symfony5MigrationDiff() {
  wex cli/exec -c="doctrine:migration:diff"
}