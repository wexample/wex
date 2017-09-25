#!/usr/bin/env bash

# Use this file to install wexample for current user
# Run : . /opt/wexample/bash/ubuntu-16.x/_installLocal.sh

WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"

# Add to PATH, will return global command to export var.
pathCommand=$(bash ${WEX_SCRIPTS_DIR}"wexample/wexample.sh" wexample/addToPath)
# Add to global PATH.
eval ${pathCommand}

# Say Hi.
echo "Wexample Script installed at vesion v"$(wex wexample/version)
wex wexample/logo
