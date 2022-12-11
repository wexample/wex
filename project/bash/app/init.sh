#!/usr/bin/env bash

# Place here namespace specific data
# that should not be accessed by other namespaces.
# TODO MANAGE CACHING
# TODO MIGRATE VARS FROM global.sh

export WEX_WEXAMPLE_APP_DIR_TMP=./tmp/
export WEX_WEXAMPLE_APP_DIR_PROJECT=./project/
export WEX_WEXAMPLE_APP_CONFIG=${WEX_WEXAMPLE_APP_DIR_TMP}config
export WEX_WEXAMPLE_APP_COMPOSE_BUILD_YML=${WEX_WEXAMPLE_APP_DIR_TMP}docker-compose.build.yml