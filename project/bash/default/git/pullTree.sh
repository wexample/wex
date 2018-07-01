#!/usr/bin/env bash

gitPullTree() {
  # Get last updates.
  git pull

  # Update submodules.
  if [ -f .gitmodules ]; then
    git submodule update --init --recursive --remote
    git pull --recurse-submodules --depth=1
  fi
}
