#!/usr/bin/env bash

coreBuildArgs() {
  _DESCRIPTION="Prepare core for new version"
  # shellcheck disable=SC2034
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
  NEW_BUILD=$((BUILD + 1))
  NEW_VERSION="${VERSION}.${NEW_BUILD}"

  wex-exec default::config/setValue \
    -f="${WEX_DIR_ROOT}includes/globals.sh" \
    -s="=" \
    -k="export WEX_CORE_VERSION" \
    -v="${NEW_VERSION}" \
    -vv

  _wexLog "Updating version in README.md"
  # Replace version in README.md
  sed -i"${WEX_SED_I_ORIG_EXT}" "s/\(.*wex v\)[0-9]*\.[0-9]*\.[0-9]*/\1${NEW_VERSION}/" "${WEX_DIR_ROOT}README.md"
  rm "${WEX_DIR_ROOT}README.md${WEX_SED_I_ORIG_EXT}"
}
