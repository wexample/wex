#!/usr/bin/env bash

# Should be ran inside a composer project.
composerUpdate() {
  # Install all project dependencies
  php composer.phar clear-cache -q
  php composer.phar update -q
}
