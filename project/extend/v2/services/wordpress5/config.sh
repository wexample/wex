#!/usr/bin/env bash

wordpress5Config() {
  # Same config as web.
  . ${WEX_DIR_ROOT}services/wordpress4/config.sh

  # Use exact same config.
  wordpress4Config
}
