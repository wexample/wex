#!/usr/bin/env bash

# Should be ran inside a composer project.
composerInstall() {
  # Install all project dependencies
  php composer.phar clear-cache -q
  php composer.phar install -q
}
