#!/usr/bin/env bash

# Use this file to install wex scripts.

WEX_LOCAL_DIR="/opt/wex/"
BASHRC_PATH=~/.bashrc

chmod -R +x ${WEX_LOCAL_DIR}

# Copy to bin
cp ${WEX_LOCAL_DIR}project/bash/wex.bin.sh /usr/local/bin/wex
chmod -R +x /usr/local/bin/wex

# Install minimal requirements
apt-get update
apt-get install \
  curl \
  net-tools \
  zip \
  -yqq
# Install Docker
wex docker/install

# Create sites folder
mkdir -p /var/www

# Add to bashrc.
wex file/textAppendOnce -f="${BASHRC_PATH}" -l=". ${WEX_LOCAL_DIR}project/bash/autocomplete.sh"

# Say Hi.
echo "Wexample Script installed at version "$(wex wex/version)
wex wex/logo
