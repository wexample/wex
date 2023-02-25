#!/usr/bin/env bash

_wexHasRealPath() {
  if [ "$(type -t realpath 2>/dev/null)" = "file" ]; then
    echo "true"
  else
    echo "false"
  fi
}

_wexVersionGetMajor() {
  sed -n "s/\([[:digit:]]\{0,\}\)\([\.].\{0,\}\)/\1/p" <<<"${1}"
}
