#!/usr/bin/env bash

mailDkim() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  # Create global config.
  CONTAINER_NAME=${SITE_NAME_INTERNAL}_mailserver
  bash ${BASH_SOURCE%/*}/_setup.sh config dkim 1024
}