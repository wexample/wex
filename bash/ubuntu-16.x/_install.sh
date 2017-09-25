#!/usr/bin/env bash

WEX_DIR_BASH_UBUNTU16="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
WEX_DIR_ROOT=${WEX_DIR_BASH_UBUNTU16}"../../"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"

cd /opt
# Remove if exists.
rm -rf wexample
# Create dir.
mkdir wexample
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample
# Install locally
bash ${WEX_DIR_BASH_UBUNTU16}_installLocal.sh
