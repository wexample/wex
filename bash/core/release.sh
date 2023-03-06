#!/usr/bin/env bash

coreReleaseArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='Push new core version to the repository'
  _ARGUMENTS=(
    'origin o "Origin repository" false origin'
  )
}

coreRelease() {
  cd "${WEX_DIR_ROOT}"

  if [ "$(wex git/hasChange)" = "true" ]; then
    _wexError "You have uncommited changes, please commit them before pushing."
    exit 1
  fi

  # Create and commit new version.
  wex core/build
  git add .
  git commit -m "RC New version : $(wex default::core/version)"

  for ADDON in "${WEX_ADDONS[@]}"; do
    _wexLog "Pushing ${ADDON}..."

    cd "${WEX_DIR_ADDONS}${ADDON}"
    git push "${ORIGIN}"
  done

  # Push at end as this will trigger the build.
  git push "${ORIGIN}"

  # Update local registry
  wex default::core/register
}
