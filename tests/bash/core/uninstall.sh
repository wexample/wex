#!/usr/bin/env bash

coreUninstallTest() {
  local FILEPATH

  FILEPATH=$(_wexTestSampleInit "bashrc")

  . ${WEX_DIR_ROOT}includes/install.sh

  wex default::file/textAppendOnce -f="${FILEPATH}" -l="${WEX_FILE_BASHRC_COMMAND}"

  wex default::file/lineRemove -f="${FILEPATH}" -l="${WEX_FILE_BASHRC_COMMAND}"

  _wexTestSampleDiff "bashrc" false "Test bashrc change has been reverted"
}
