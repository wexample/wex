#!/usr/bin/env bash

bashAddToPath() {
  # Add now.
  export PATH=$PATH:${1}
  # Add to path.
  bash ${WEX_DIR_ROOT}'wexample.sh' fileTextAppend ~/.bashrc 'export PATH=$PATH:'${1}
}
