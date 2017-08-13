#!/usr/bin/env bash

WEX_DIR_BASH_UBUNTU16="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
WEX_DIR_ROOT=${WEX_DIR_BASH_UBUNTU16}"../../"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"
WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"

cd /opt
# Remove if exists.
rm -rf wexample
# Create dir.
mkdir wexample
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample
# Add permission to execute
chmod +x "${WEX_LOCAL_DIR}bash/wexample"
# Add to PATH, will return global command to export var.
pathCommand=$(bash ${WEX_SCRIPTS_DIR}"wexample.sh" systemPathAdd "${WEX_LOCAL_DIR}bash")
# Add to global PATH.
eval ${pathCommand}

# Say Hi.
echo "Wexample Script installed at vesion v"$(wexample wexampleVersion)
wexample wexampleLogo
