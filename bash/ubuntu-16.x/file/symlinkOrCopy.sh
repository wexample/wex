#!/usr/bin/env bash

fileSymlinkOrCopyArgs() {
  _ARGUMENTS=(
    [0]='from f "Symlink location" true'
    [1]='target t "Target" true'
  )
}

fileSymlinkOrCopy() {
  # Symlink does not exists
  if [ ! -L ${TARGET} ]; then
    # Try to make a symlink, may fail on Windows docker context.
    if ! ln -sf ${FROM} ${TARGET} &>/dev/null; then
      # Create a copy
      cp -r ${FROM} ${TARGET}
    fi;
  fi;
}
