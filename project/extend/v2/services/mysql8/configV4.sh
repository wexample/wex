#!/usr/bin/env bash

mysql8ConfigV4() {
  # TODO Import and rewrite v3 config.
  echo "Set DB_CONTAINER to mysql8"
  # Change main container name only.
  wex config/setValue -f=tmp/config -k=DB_CONTAINER -v="mysql8" -s="="
}
