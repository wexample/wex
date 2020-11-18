#!/usr/bin/env bash

composerOutdated() {
  wex site/exec -l -c="composer show -l --direct --format json > ../tmp/outdated.json"

  echo ../tmp/outdated.json
}