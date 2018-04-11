#!/usr/bin/env bash

wexVersion() {
  # Go to git repo.
  cd ${WEX_DIR_ROOT}../
  # Just get current tag.
  wex git/currentTag
}
