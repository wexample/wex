#!/usr/bin/env bash

wexampleInstall() {
  cd /opt
  # Remove if exists.
  rm -rf wexample
  # Create dir
  mkdir wexample
  # Get whole repository.
  git clone ${WEX_URL_GITHUB}scripts.git wexample
  # Add to PATH.
  "${WEX_DIR_ROOT}wexample.sh" bashAddToPath '/opt/wexample/bash/ubuntu16.x/'
}
