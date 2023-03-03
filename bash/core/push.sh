#!/usr/bin/env bash

corePushArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='Push new core version to the repository'
  _ARGUMENTS=(
    'origin o "Origin repository" false origin'
  )
}

corePush() {
  cd "${WEX_DIR_ROOT}"

  if [ "$(wex git/hasChange)" = "true" ];then
    _wexError "You have uncommited changes, please commit them before pushing."
    exit 1
  fi

  # Create and commit new version.
  wex core/build
  git add .
  git commit -m "New version"
  git push "${ORIGIN}"

  for ADDON in "${WEX_ADDONS[@]}"; do
      _wexLog "Pushing ${ADDON}..."

      cd "${WEX_DIR_ADDONS}${ADDON}"
      git push "${ORIGIN}"
  done
}
