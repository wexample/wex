#!/usr/bin/env bash

# Used in production to retrieve changes when tests are passed.
sitePull() {
  ${WEX_DIR_V3_CMD} app::app/pull
}
