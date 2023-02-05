#!/usr/bin/env bash

# Use this file to install wex scripts.
# This file should be able to be executed several times
# even script are already installed.
# We don't include external packages install which are
# managed by `wex core::requirements/install` script.

. /opt/wex/includes/globals.sh
. "${WEX_DIR_ROOT}/includes/function/install.sh"

# Check user is root
if [ "${EUID}" -gt 0 ];then
  _wexLog "Install needs sudo, switching.."

  # Exec as sudo, but keep some environment vars.
  ${WEX_SWITCH_SUDO_COMMAND} bash "${BASH_SOURCE[0]}"
  exit
fi

WEX_BASH_VERSION_MIN='5'
WEX_BIN="/usr/local/bin/wex"
WEX_FILE_BASHRC_HANDLER="${WEX_DIR_ROOT}bash/bashrc-handler.sh"

# Set permission on base folder.
_wexLog "Set all permissions on ${WEX_DIR_ROOT}"
chmod -R +x "${WEX_DIR_ROOT}"

# Check shell version.
if [ -z ${WEX_BASH_VERSION+x} ]; then
  WEX_BASH_VERSION=$(_wexVersionGetMajor "${BASH_VERSION}")
  if [ "${WEX_BASH_VERSION}" -lt "${WEX_BASH_VERSION_MIN}" ]; then
    _wexError "Wex error, need to run on bash version ${WEX_BASH_VERSION_MIN}" "Your current version is ${WEX_BASH_VERSION}"
    exit
  fi;
fi;

# Check if "realpath" method exists (missing on raw macos)
if [ "$(_wexHasRealPath)" = "false" ]; then
  _wexError "The realpath method is not found" "You may install coreutils to solve it"
  exit;
fi;

# Create or recreate symlink.
_wexLog "Adding symlink.."
if [ -L ${WEX_BIN} ];then
  rm "${WEX_BIN}"
fi

_wexLog "Create env default file."
if [ ! -f "${WEX_DIR_ROOT}${WEX_DIR_APP_DATA}.env" ];then
  echo "APP_ENV=prod" > "${WEX_DIR_ROOT}${WEX_DIR_APP_DATA}.env"
fi

# Symlink to bin
ln -fs "${WEX_DIR_ROOT}bash/wex.bin.sh" ${WEX_BIN}
chmod -R +x ${WEX_BIN}

# Now the "wex" command is working, we can use it internally.

# Install core scripts dependencies
_wexLog "Installing core scripts dependencies in ${WEX_DIR_BASH}"
wex scripts/install -d="${WEX_DIR_BASH}"

# Create apps folder
_wexLog "Creates /var/www folder for apps management"
mkdir -p /var/www
_wexLog "Creates ${WEX_RUNNER_PATH_WEX} folder for apps management"
mkdir -p "${WEX_RUNNER_PATH_WEX}"

_wexLog "Fixing permissions..."
chown "${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}" "${WEX_RUNNER_PATH_WEX}"
chown -R "${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}" "${WEX_DIR_ROOT}"

# Add to bashrc, create it if not exists.
_wexLog "Adding autocompletion script to ${WEX_RUNNER_BASHRC_PATH}"
touch "${WEX_RUNNER_BASHRC_PATH}"
wex file/textAppendOnce -f="${WEX_RUNNER_BASHRC_PATH}" -l=". ${WEX_FILE_BASHRC_HANDLER}"

_wexLog "Installing addons..."
for ADDON in "${WEX_ADDONS[@]}"; do
  if [ ! -d "${WEX_DIR_ADDONS}${ADDON}" ]; then
    _wexLog "Cloning addon : ${ADDON}"
    git clone --depth=1 "https://github.com/wexample/wex-addon-${ADDON}.git" "${WEX_DIR_ADDONS}${ADDON}"
  else
    _wexLog "Addon dir exists : ${WEX_DIR_ADDONS}${ADDON}"
  fi
done

_wexLog "Registering..."
wex default::core/register

_wexLog "Install complete..."

wex core/logo
