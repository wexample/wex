#!/usr/bin/env bash

WEX_DIR_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"
WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"

cd /opt
# Remove if exists.
rm -rf wexample
# Create dir
mkdir wexample
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample
# Load used methods.
. ${WEX_SCRIPTS_DIR}"fileTextAppend.sh"
. ${WEX_SCRIPTS_DIR}"bashAddToPath.sh"
# Add to PATH
bashAddToPath "/opt/wexample/bash"
