#!/usr/bin/env bash

bashAddToPath() {
  command="export PATH=$PATH:${1}"
  # Add now.
  eval ${command}
  # Add to path.
  ${WEX_DIR_ROOT}wexample.sh fileTextAppend ~/.bashrc "${command}"
}
