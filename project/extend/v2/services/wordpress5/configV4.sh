#!/usr/bin/env bash

wordpress5ConfigV4() {
  # TODO Import and rewrite v3 config.
  echo "  > Wordpress container set to wordpress5"
  # Change main container name only.
  wex config/changeValue -f=tmp/config -k=SITE_CONTAINER -v="wordpress5" -s="="
}
