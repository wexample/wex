#!/usr/bin/env bash

# Should be ran inside a composer project.
composerUpdate() {
  # Install all project dependencies
  composer clear-cache -q
  composer update -q
}
