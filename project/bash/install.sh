#!/usr/bin/env bash

. /opt/wex/project/bash/globals.sh

# Check user is root
if [ "${EUID}" -gt 0 ];then
  _wexLog "Install needs sudo, switching.."

  # Exec as sudo
  sudo bash "${BASH_SOURCE[0]}"
  exit
fi

# Set permission on base folder.
_wexLog "Set all permissions on ${WEX_DIR_INSTALL}"
chmod -R +x "${WEX_DIR_INSTALL}"
