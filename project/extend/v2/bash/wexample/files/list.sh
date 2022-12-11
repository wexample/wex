#!/usr/bin/env bash

filesList() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  . .wex

  # Print on new lines
  printf '%s\n' "${FILES[@]}"
}
