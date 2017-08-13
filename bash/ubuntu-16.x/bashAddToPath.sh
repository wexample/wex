#!/usr/bin/env bash

bashAddToPath() {
  if [[ ":$PATH:" != *":${1}"* ]]; then
    # Print command to add, need to execute it into global context.
    echo $("export PATH=$PATH:${1}")
    # Add to path.
    bash ${WEX_DIR_BASH_UBUNTU16}'wexample.sh' fileTextAppendOnce ~/.bashrc 'export PATH=$PATH:'${1}
  fi
}
