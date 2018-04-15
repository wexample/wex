#!/usr/bin/env bash

export WEX_WEXAMPLE_DIR_TMP=${WEX_DIR_TMP}"wexample/"
export WEX_WEXAMPLE_DIR_PROXY_TMP=${WEX_WEXAMPLE_DIR_TMP}"proxy/"
export WEX_WEXAMPLE_PROXY_CONTAINER="wex_reverse_proxy"
export WEX_WEXAMPLE_SITE_DIR_TMP="./tmp/"
export WEX_WEXAMPLE_SITE_CONFIG=${WEX_WEXAMPLE_SITE_DIR_TMP}config
export WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML=${WEX_WEXAMPLE_SITE_DIR_TMP}"docker-compose.build.yml"
export WEX_WEXAMPLE_ENVIRONMENTS=(local dev prod)
export WEX_GITLAB_URL="gitlab.wexample.com"
