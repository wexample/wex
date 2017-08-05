#!/usr/bin/env bash

cd /opt
# Remove if exists.
rm -rf wexample
# Create dir
mkdir wexample
# Get whole repository.
git clone ${WEX_URL_GITHUB}scripts.git wexample

. "/opt/wexample/bash/ubuntu-16.x/bashAddToPath.sh"

bashAddToPath "/opt/wexample/wexample"
