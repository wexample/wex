#!/usr/bin/env bash

bashAddToPath() {
  echo "Add to path "$PATH
  # Add now.
  export PATH=$PATH:"${1}"
  # Add to path.
  bash ${WEX_DIR_ROOT}'wexample.sh' fileTextAppend ~/.bashrc 'export PATH=$PATH:'${1}
}
