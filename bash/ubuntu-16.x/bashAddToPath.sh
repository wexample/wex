#!/usr/bin/env bash

bashAddToPath() {
  if [[ ":$PATH:" != *":${1}"* ]]; then
    # Add now.
    export PATH=$PATH":${1}"
    # Add to path.
    bash ${WEX_DIR_BASH_UBUNTU16}'wexample.sh' fileTextAppendOnce ~/.bashrc 'export PATH=$PATH:'${1}
    # Reload.
    . ~/.bashrc
  fi
}
