#!/usr/bin/env bash

# Used in production to retrieve changes when tests are passed.
sitePull() {
  # Use new version
  ${WEX_DIR_V3_CMD} app::app/pull
}
