#!/usr/bin/env bash

# Use this file to install wex scripts.
# This file should be able to be executed several times
# even script are already installed.
# We don't include external packages install which are
# managed by `wex core::requirements/install` script.

WEX_BASH_VERSION_MIN='5'
WEX_BIN="/usr/local/bin/wex"

. /opt/wex/project/bash/globals.sh
. "${WEX_DIR_BASH}/includes/install.sh"

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

# Check shell version.
if [ -z ${WEX_BASH_VERSION+x} ]; then
  WEX_BASH_VERSION=$(_wexVersionGetMajor "${BASH_VERSION}")
  if [ "${WEX_BASH_VERSION}" -lt ${WEX_BASH_VERSION_MIN} ]; then
    _wexError "Wex error, need to run on bash version "${WEX_BASH_VERSION_MIN} "Your current version is ${WEX_BASH_VERSION}"
    exit
  fi;
fi;

# Check if "realpath" method exists (missing on raw macos)
if [ "$(_wexHasRealPath)" = "false" ]; then
  _wexError "The realpath method is not found" "You may install coreutils to solve it"
  exit;
fi;

# Create or recreate symlink.
[ -e "${WEX_BIN}" ] && rm "${WEX_BIN}"
# Symlink to bin
ln -s ${WEX_DIR_INSTALL}project/bash/wex.bin.sh ${WEX_BIN}
chmod -R +x ${WEX_BIN}

# Create sites folder
mkdir -p /var/www
