#!/usr/bin/env bash

wexampleInstall() {
  cd /opt
  # Create dir
  mkdir wexample
  cd wexample
  # Get whole repository.
  git clone ${WEX_URL_GITHUB}scripts.git .
  # Add to path
  bash/ubuntu-16.x/wexample.sh fileTestAppend ~/.bashrc export PATH=/opt/wexample/bash/ubuntu-16.x/
}
