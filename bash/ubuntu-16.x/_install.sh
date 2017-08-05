#!/usr/bin/env bash

. "_variables.sh"

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
