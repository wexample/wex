#!/usr/bin/env bash

_wexMigrateCore() {
  if [ $(wex dir/exists -d="/opt/wexample") == true ];then
    # Move core to a new location.
    mv /opt/wexample /opt/wex
  fi
}

_wexMigrateApp() {
  echo "APP"

  # TODO SITE_NAME_INTERNAL
  # TODO site/test to app/test into script folder
}