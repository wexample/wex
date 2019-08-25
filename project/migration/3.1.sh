#!/usr/bin/env bash

_wexMigrateCore() {
  # Move core to a new location.
  mv /opt/wexample /opt/wex
}

_wexMigrateApp() {
  echo "APP"
}