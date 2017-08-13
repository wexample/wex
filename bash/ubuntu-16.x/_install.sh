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
# Load used methods.
. ${WEX_SCRIPTS_DIR}"wexample.sh"
# Add to PATH, will return global command to export var.
eval $(wexample bashAddToPath "${WEX_LOCAL_DIR}bash")
# Add perm.
chmod +x "${WEX_LOCAL_DIR}bash/wexample"

# Say Hi.
echo "Wexample Script installed at vesion v"$(wexample wexampleVersion)
wexample wexampleLogo
