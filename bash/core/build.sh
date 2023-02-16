#!/usr/bin/env bash

coreBuildArgs() {
  _DESCRIPTION="Update core data. Should be executed before deploying."
}

coreBuild() {
  _wexLog "Updating variables in globals.sh"

  wex default::config/setValue \
    -f="${WEX_DIR_ROOT}includes/globals.sh" \
    -s="=" \
    -k="WEX_ADDONS" \
    -v="($(wex addons/list))" \
    -vv
}
