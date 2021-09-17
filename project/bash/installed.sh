#!/usr/bin/env bash
# Return "true" if wex script are properly installed.

wex_installed() {
  # wex command should be accessible globally.
  if [ "$(type -t wex)" = file ];then
    # Test if wex hi command runs.
    if [ $(wex hi | xargs) = "hi!" ]; then
      echo true
      return
    fi
  fi

  echo false
}

wex_installed
