#!/usr/bin/env bash

# Used in production to retrieve changes when tests are passed.
sitePull() {
  # Update GIT and submodules.
  wex git/pullTree
  # Execute service script.
  wex service/exec -c=sitePull
  # Rebuild and clear caches.
  wex site/build
  # Execute local scripts.
  wex hook/exec -c=pull
  # Allow cron update without reloading whole site.
  wex cron/reload
}
