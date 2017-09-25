#!/usr/bin/env bash

WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"

# Add permission to execute
chmod +x "${WEX_LOCAL_DIR}bash/wexample"
# Add to PATH, will return global command to export var.
pathCommand=$(bash ${WEX_SCRIPTS_DIR}"wexample/wexample.sh" system/pathAdd "${WEX_LOCAL_DIR}bash")
# Add to global PATH.
eval ${pathCommand}

# Say Hi.
echo "Wexample Script installed at vesion v"$(wex wexample/version)
wex wexample/logo
