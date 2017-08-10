#!/usr/bin/env bash

bashOsName() {
  case "$(uname -s)" in
    Darwin)
      echo 'mac'
      ;;
    Linux)
      echo 'linux'
      ;;
    CYGWIN*|MINGW32*|MSYS*)
      echo 'windows'
      ;;
    # Add here more strings to compare
    # See correspondence table at the bottom of this answer
    *)
      echo 'other OS'
      ;;
  esac
}
