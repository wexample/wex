#!/usr/bin/env bash

wordpressDisableAllPlugins() {
  . .wex

  wex db/exec -c="UPDATE ${WP_DB_TABLE_PREFIX}options SET option_value='' WHERE option_name='active_plugins'"
}