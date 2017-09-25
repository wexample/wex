#!/usr/bin/env bash

WEX_LOCAL_DIR="/opt/wexample/"
WEX_URL_GITHUB="https://github.com/wexample/"

cd /opt
# Remove if exists.
rm -rf ${WEX_LOCAL_DIR}
# Create dir.
mkdir ${WEX_LOCAL_DIR}
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample
# Install locally
bash ${WEX_LOCAL_DIR}bash/ubuntu-16.x/_installLocal.sh
