#!/usr/bin/env bash

wexampleInstall() {
  cd /opt
  # Create dir
  mkdir wexample
  # Get whole repository.
  git clone ${WEX_URL_GITHUB}scripts.git wexample
  # Add to path
  bash wexample/bash/ubuntu-16.x/wexample.sh fileTestAppend ~/.bashrc export PATH=/opt/wexample/bash/ubuntu-16.x/
}
