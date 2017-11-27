#!/usr/bin/env bash

# Use this file to install wexample for current user
# Run : . /opt/wexample/bash/ubuntu-16.x/_installLocal.sh

WEX_LOCAL_DIR="/opt/wexample/"

# Add to PATH, will return global command to export var.
pathCommand=$(bash ${WEX_LOCAL_DIR}"bash/wexample.sh" wex/addToPath)
# Add to global PATH.
eval ${pathCommand}

# Say Hi.
echo "Wexample Script installed at version v"$(wex wex/version)
wex wex/logo
