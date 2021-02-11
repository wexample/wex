#!/usr/bin/env bash

wordpress5ConfigV4() {
  # TODO Import and rewrite v3 config.
  echo "  > Set SITE_CONTAINER to wordpress5"
  # Change main container name only.
  wex config/changeValue -f=tmp/config -k=SITE_CONTAINER -v="wordpress5" -s="="

  . .wex
  # Set values
  wex config/setValue -f=tmp/config -k=WP_DB_TABLE_PREFIX -v="${WP_DB_TABLE_PREFIX}" -s="="
}
