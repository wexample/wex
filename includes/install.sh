#!/usr/bin/env bash

export WEX_BASH_VERSION_MIN='5'
export WEX_BIN="/usr/local/bin/wex"
export WEX_FILE_BASHRC_HANDLER="${WEX_DIR_ROOT}bash/bashrc-handler.sh"
export WEX_FILE_BASHRC_COMMAND=". ${WEX_FILE_BASHRC_HANDLER}"
export WEX_BASHRC_PATH=~/.bashrc
