#!/usr/bin/env bash

# Use this file to install wex scripts.

. /opt/wex/project/bash/globals.sh

chmod -R +x ${WEX_DIR_INSTALL}

# Copy to bin
cp ${WEX_DIR_INSTALL}project/bash/wex.bin.sh /usr/local/bin/wex
chmod -R +x /usr/local/bin/wex

# Create sites folder
mkdir -p /var/www

# Add to bashrc.
wex file/textAppendOnce -f="${BASHRC_PATH}" -l=". ${WEX_DIR_INSTALL}project/bash/autocomplete-handler.sh"

# Say Hi.
echo "Wexample Script installed at version "$(wex wex/version)
wex wex/logo
