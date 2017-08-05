#!/usr/bin/env bash

wexampleInstall() {
  cd /opt
  # Create dir
  mkdir wexample
  # Get whole repository.
  git clone ${WEX_URL_GITHUB}scripts.git wexample
  # Add to path
  bash/ubuntu-16.x/wexample.sh fileTextAppend ~/.bashrc export PATH=/opt/wexample/bash/ubuntu-16.x/
}
