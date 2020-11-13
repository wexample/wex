#!/usr/bin/env bash

sitePushArgs() {
  _ARGUMENTS=(
    [0]='no_push np "Execute script only, git push will be executed outside (maybe from pre-push)." false'
  )
}

sitePush() {
  wex ci/exec -c=push

  if [ -z "${NO_PUSH+x}" ]; then
    # From local to Gitlab server which will run automated tests.
    git push --tags
  fi;
}
