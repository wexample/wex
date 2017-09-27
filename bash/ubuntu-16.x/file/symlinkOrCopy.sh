#!/usr/bin/env bash

fileSymlinkOrCopyArgs() {
  _ARGUMENTS=(
    [0]='from f "Symlink location" true'
    [1]='target t "Target" true'
    [2]='recursive r "Recursive : create subfolder if not exists" false'
  )
}

fileSymlinkOrCopy() {

  # Create sub directory
  if [ -z "${RECURSIVE+x}" ];then
    # Create whole path
    mkdir -p ${TARGET}
    # Remove just last piece.
    rm -rf ${TARGET}
  fi;

  # Symlink does not exists
  if [ ! -L ${TARGET} ]; then
    # Try to make a symlink, may fail on Windows docker context.
    if ! ln -sf ${FROM} ${TARGET} &>/dev/null; then
      # Create a copy
      cp -r ${FROM} ${TARGET}
    fi;
  fi;
}
