#!/usr/bin/env bash

# Use this file to install wex scripts.
# This file should be able to be executed several times
# even script are already installed.
# We also avoid to include external packages install which are
# managed by `wex core::requirements/install` script.

. /opt/wex/project/bash/globals.sh

# Check shell version.
_wexBashCheckVersion
# Check if "realpath" method exists (missing on raw macos)
if [[ $(_wexHasRealPath) == "false" ]]; then
  _wexError "The realpath method is not found" "You may install coreutils to solve it"
  exit;
fi;

chmod -R +x ${WEX_DIR_INSTALL}
# Copy to bin
cp ${WEX_DIR_INSTALL}project/bash/wex.bin.sh /usr/local/bin/wex
chmod -R +x /usr/local/bin/wex

# Create sites folder
mkdir -p /var/www

# Add to bashrc, create it if not exists.
touch ${BASHRC_PATH}
wex file/textAppendOnce -f="${BASHRC_PATH}" -l=". ${WEX_DIR_INSTALL}project/bash/autocomplete-handler.sh"

# A hooks to git in case of contributing.
cd ${WEX_DIR_INSTALL}
wex git/initHooks

# Activate autocomplete.
. ${BASHRC_PATH}

# Say Hi.
echo "wex installed at version "$(wex core/version)
wex core/logo

. ${WEX_DIR_BASH}/colors.sh

wex core::requirements/list

if [[ $(wex core::requirements/installed) == false ]];then
  printf "\n${WEX_COLOR_CYAN}You may want to install app requirements by typing${WEX_COLOR_RESET}\n"
  printf "${WEX_COLOR_YELLOW}wex core::requirements/install${WEX_COLOR_RESET}"
fi

echo ""