#!/usr/bin/env bash

coreBuildArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Update core data. Should be executed before deploying."
}

coreBuild() {
  _wexLog "Updating permissions"
  cd "${WEX_DIR_ROOT}"
  chmod 755 -R ./

  _wexLog "Updating variables in globals.sh"

  wex-exec default::config/setValue \
    -f="${WEX_DIR_ROOT}includes/globals.sh" \
    -s="=" \
    -k="WEX_ADDONS" \
    -v="($(wex-exec addons/list))" \
    -vv

  # Increment core version

  local NEW_VERSION
  NEW_VERSION=$(wex default::version/increment -t=minor -v="${WEX_CORE_VERSION}")

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
