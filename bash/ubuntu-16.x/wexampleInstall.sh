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
  bash '/opt/wexample/bash/ubuntu-16.x/wexample.sh' bashAddToPath '/opt/wexample/'
  echo "Installed wexample v"$(wexample wexampleVersion)
}
