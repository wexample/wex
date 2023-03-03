#!/usr/bin/env bash

coreUninstallArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='Uninstall wex.'
  _ARGUMENTS=(
    'file f "Custom bashrc file path" false'
  )
}

coreUninstall() {
  rm -rf "${WEX_DIR_ROOT}"

  . /opt/wex/includes/install.sh

  local BASHRC=${FILE:-${WEX_BASHRC_PATH}}
  wex default::file/lineRemove -f="${BASHRC}" -l="${WEX_FILE_BASHRC_COMMAND}"
}
