#!/usr/bin/env bash

siteBuild() {
  # Clear site cache.
  wex cache/clear
  # Rebuild assets.
  wex hook/exec -c=build
  # Reset permissions.
  wex site/perms
}
