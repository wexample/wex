#!/usr/bin/env bash

wexVersion() {
  # Go to git repo.
  cd ${WEX_DIR_ROOT}../
  # Concat to commit number-branch
  echo ${WEX_VERSION}'.'$(git rev-list --all --count)"-"$(git rev-parse --abbrev-ref HEAD)
}
