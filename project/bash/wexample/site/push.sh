#!/usr/bin/env bash

sitePush() {
  # Execute custom script for site.
  if [ -f ci/push.sh ];then
    . ci/push.sh
  fi

  # From local to Gitlab server which will run automated tests.
  git push
}
