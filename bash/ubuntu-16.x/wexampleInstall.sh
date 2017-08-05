#!/usr/bin/env bash

wexampleInstall() {
  cd /opt
  # Create dir
  mkdir wexample
  # Get whole repository.
  git clone ${WEX_URL_GITHUB}scripts.git wexample
  # Add to PATH.
  "${WEX_DIR_CURRENT}wexample.sh" bashAddToPath ${WEX_DIR_CURRENT}
}
