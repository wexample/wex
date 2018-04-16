#!/usr/bin/env bash

# Use this file to install wexample for current user
# Run : . /opt/wexample/project/bash/ubuntu-16.x/_installLocal.sh

WEX_LOCAL_DIR="/opt/wexample/"

chmod -R +x ${WEX_LOCAL_DIR}

# Copy to bin
cp ${WEX_LOCAL_DIR}project/bash/wex.bin.sh /usr/local/bin/wex
chmod -R +x /usr/local/bin/wex

# Say Hi.
echo "Wexample Script installed at version "$(wex wex/version)
wex wex/logo
