#!/usr/bin/env bash

WEX_DIR_BASH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/
WEX_DIR_ROOT=$(dirname "${WEX_DIR_BASH}")"/"
WEX_DIR_INSTALL=$(dirname "${WEX_DIR_ROOT}")"/"
WEX_SCREEN_WIDTH=$([ "${TERM}" != "unknown" ] && tput cols || echo 100)

export WEX_DIR_BASH
export WEX_DIR_INSTALL
export WEX_DIR_ROOT
export WEX_SCREEN_WIDTH

. "${WEX_DIR_BASH}/includes/common.sh"
. "${WEX_DIR_BASH}/includes/message-default.sh"
. "${WEX_DIR_BASH}/colors.sh"
