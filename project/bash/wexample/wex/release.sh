#!/usr/bin/env bash

# Executed on wexample production server to
# create a new release of wex scripts.
wexRelease() {
  cd ${WEX_DIR_ROOT}../

  # Push with tags.
  wex site/push
}
