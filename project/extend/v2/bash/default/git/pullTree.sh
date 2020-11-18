#!/usr/bin/env bash

gitPullTree() {
  local SUCCESS=true

  # Get last updates.
  if /usr/bin/git pull;then
    # Update submodules.
    if [ -f .gitmodules ]; then
      git submodule update --init --recursive --remote

      if ! /usr/bin/git pull --recurse-submodules;then
        SUCCESS=false
      fi
    fi
  else
    SUCCESS=false
  fi

  echo ${SUCCESS}
}
