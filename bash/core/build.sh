#!/usr/bin/env bash

coreBuildArgs() {
  _DESCRIPTION="Update core data. Should be executed before deploying."
}

coreBuild() {
  _wexLog "Updating variables in globals.sh"

  wex-exec default::config/setValue \
    -f="${WEX_DIR_ROOT}includes/globals.sh" \
    -s="=" \
    -k="WEX_ADDONS" \
    -v="($(wex-exec addons/list))" \
    -vv

  # Increment core version

  local VERSION_ACTUAL
  local VERSION
  local BUILD
  local NEW_BUILD

  VERSION_ACTUAL=$(wex-exec core/version)
  VERSION=$(echo "${VERSION_ACTUAL}" | cut -d '.' -f 1-2)
  BUILD=$(echo "${VERSION_ACTUAL}" | cut -d '.' -f 3)

  # Increment.
  NEW_BUILD=$((BUILD+1))

  wex-exec default::config/setValue \
    -f="${WEX_DIR_ROOT}includes/globals.sh" \
    -s="=" \
    -k="export WEX_CORE_VERSION" \
    -v="${VERSION}.${NEW_BUILD}" \
    -vv
}
