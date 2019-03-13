#!/usr/bin/env bash

siteReset() {
  # Clear site cache.
  wex cache/clear
  # Rebuild assets.
  wex site/build
  # Reset permissions.
  wex site/perms
}