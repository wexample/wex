#!/usr/bin/env bash

symfony5MigrationCreate() {
  wex cli/exec -c="doctrine:migration:generate"
}