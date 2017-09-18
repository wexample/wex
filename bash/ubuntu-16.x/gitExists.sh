#!/usr/bin/env bash

gitExists() {
  git --version 2>&1 >/dev/null
  GIT_IS_AVAILABLE=$?
  if [ ${GIT_IS_AVAILABLE} -eq 0 ]; then
    echo true
   else
    echo false
  fi;
}
