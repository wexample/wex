#!/usr/bin/env bash

_wexMigrateCore() {
  if [ $(wex dir/exists -d="/opt/wexample") == true ];then
    # Move core to a new location.
    mv /opt/wexample /opt/wex
  fi
  # Reinstall.
  bash /opt/wex/install
}