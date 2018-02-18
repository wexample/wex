#!/usr/bin/env bash

siteBuild() {
  # Execute custom script for site.
  if [ -f ci/build.sh ];then
    . ci/build.sh
  fi
}
