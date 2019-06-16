#!/usr/bin/env bash

# Used in production to retrieve changes when tests are passed.
sitePull() {
  # Update GIT and submodules.
  wex git/pullTree
  # Execute service script.
  wex service/exec -c=sitePull
  # Execute pull action for found framework.
  wex framework/exec -c=pull
  # Execute local scripts.
  wex ci/exec -c=pull
  # Allow cron update without reloading whole site.
  wex cron/reload
}
