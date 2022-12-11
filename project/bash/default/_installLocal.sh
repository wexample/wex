#!/usr/bin/env bash

# Use this file to install wexample for current user
# Run : . /opt/wexample/project/bash/default/_installLocal.sh

WEX_LOCAL_DIR="/opt/wexample/"

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

# Say Hi.
echo "Wexample Script installed at version "$(wex core/version)
wex wex/logo
