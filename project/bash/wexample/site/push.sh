#!/usr/bin/env bash

sitePush() {
  wex ci/exec -c=push

  # From local to Gitlab server which will run automated tests.
  git push --tags
}
