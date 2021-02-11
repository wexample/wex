#!/usr/bin/env bash

mysqlConfigV4() {
  # TODO Import and rewrite v3 config.
  echo "  > Set DB_CONTAINER to mysql"
  # Change main container name only.
  wex config/setValue -f=tmp/config -k=DB_CONTAINER -v="mysql" -s="="
}
