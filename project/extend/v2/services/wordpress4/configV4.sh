#!/usr/bin/env bash

wordpress4ConfigV4() {
  # TODO Import and rewrite v3 config.
  echo "  > Set SITE_CONTAINER to wordpress4"
  # Change main container name only.
  wex config/changeValue -f=tmp/config -k=SITE_CONTAINER -v="wordpress4" -s="="
}
