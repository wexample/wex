#!/usr/bin/env bash

# Define proxy path.
export WEX_WEXAMPLE_DIR_PROXY=$([[ "$(uname -s)" == Darwin ]] && echo /Users/wex/server || echo /opt/wex_server/)
