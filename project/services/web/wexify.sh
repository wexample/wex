#!/usr/bin/env bash

webAppWexify() {
  mkdir -p ./.project
  # Move all content into project except dotted files
  mv ./* ./.project
  # Change name
  mv ./.project ./project
  # Get current dir name
  local CURRENT_DIR
  CURRENT_DIR=$(basename "$(realpath .)")
  # Move up
  cd ../
  # Move dotted files
  mv "${CURRENT_DIR}/.*" "${CURRENT_DIR}/project"
}