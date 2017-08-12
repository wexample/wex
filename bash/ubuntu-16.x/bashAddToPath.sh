#!/usr/bin/env bash

bashAddToPath() {
  if [[ ":$PATH:" != *":${1}"* ]]; then
    echo "Line does not exists"
    ls -la ~/
    # Add now.
    export PATH=$PATH":${1}"
    echo " WEX ? ${WEX_DIR_BASH_UBUNTU16}wexample.sh"
    # Add to path.
    bash ${WEX_DIR_BASH_UBUNTU16}'wexample.sh' fileTextAppendOnce ~/.bashrc 'export PATH=$PATH:'${1}
  fi
}
