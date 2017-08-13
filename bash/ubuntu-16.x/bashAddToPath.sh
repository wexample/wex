#!/usr/bin/env bash

bashAddToPath() {
  if [[ ":$PATH:" != *":${1}"* ]]; then
    command='export PATH="'$PATH:${1}'"'
    # Print command to add, need to execute it into global context.
    echo ${command}
    # Add to path.
    bash ${WEX_DIR_BASH_UBUNTU16}'wexample.sh' fileTextAppendOnce ~/.bashrc ${command}
  fi
}
