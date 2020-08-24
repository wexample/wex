#!/usr/bin/env bash

wordpressVersion() {
  # Use default container if missing
  local CONTAINER
  local TEMP_VERSION_FILE

  CONTAINER=$(wex app/container -c="")
  TEMP_VERSION_FILE=${WEX_WEXAMPLE_APP_DIR_TMP}wp-version.php

  docker cp "${CONTAINER}":${WEX_CONTAINER_PROJECT_DIR}/wp-includes/version.php "${TEMP_VERSION_FILE}"

  wex default::wordpress/version -f="${TEMP_VERSION_FILE}"

  rm "${TEMP_VERSION_FILE}"
}