#!/usr/bin/env bash

mailHelp() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  # Create global config.
  CONTAINER_NAME=${SITE_NAME}_mailserver
  # This show help.
  bash ${BASH_SOURCE%/*}/_setup.sh
}