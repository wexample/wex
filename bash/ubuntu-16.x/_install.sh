#!/usr/bin/env bash

# This install file can only be used by root account.

WEX_LOCAL_DIR="/opt/wexample/"
WEX_URL_GITHUB="https://github.com/wexample/"

cd /opt
# Remove if exists.
rm -rf ${WEX_LOCAL_DIR}
# Create dir.
mkdir ${WEX_LOCAL_DIR}
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample
# Add permission to execute
chmod -R +x "${WEX_LOCAL_DIR}"
# Install locally
bash ${WEX_LOCAL_DIR}bash/ubuntu-16.x/_installLocal.sh
