#!/usr/bin/env bash

wexUpdate() {
  local WEX_VERSION_BASE=$(wex wex/version)
  local WEX_VERSION_BASE=2

  # Go to wexample install dir.
  cd ${WEX_DIR_ROOT}../
  BRANCH=$(git rev-parse --abbrev-ref HEAD)

  # Override changes and pull.
  wex git/resetHard
  git fetch --tags

  # Get only last data
  git pull origin ${BRANCH}
  git update-index --chmod=+x

  local WEX_VERSION_NEW=$(wex wex/version)

  wex wex/migrate --from ${WEX_VERSION_FROM} --to ${WEX_VERSION_NEW} --command core

  _wexMessage "wex up-to-date at v"${WEX_VERSION_NEW}
}
